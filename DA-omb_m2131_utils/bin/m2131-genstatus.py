#!/usr/bin/env python

'''
Author: Thomas Brookshire

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
'''

__author = "Thomas Brookshire"
__updated = 20240613
__version = '1.3.3'
__license = 'GPLv3'

import sys
import os
import re
from time import sleep
import traceback as tb

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import \
    dispatch, GeneratingCommand, Configuration, Option, validators
from splunklib.binding import HTTPError
import splunklib.client as splc
import splunklib.results as splr
import splunklib.data as spld

@Configuration(type='reporting')
class M2131GenStatusCommand(GeneratingCommand):

    group = Option(
        doc='''
            **Syntax:** **group=***<group>*
            **Description:** The display name of the group to be tracked.''',
        require=False, default=None, validate=str)

    preview = Option(
        doc='''
            **Syntax:** **preview=***[[false]|true]*
            **Description:** Only shows the contents of the lookup file that will be created and does not create them. (default: 'true')''',
        require=False, default=True, validate=validators.Boolean())

    private = Option(
        doc='''
            **Syntax:** **private=***[[false]|true]*
            **Description:** Whether or not the the lookup file and definition will be private. If 'false', the macro will be created/updated. (default: 'true')''',
        require=False, default=True, validate=validators.Boolean())
    

    def __err(self, error):
        """(v1.0.0)"""
        if isinstance(error, str):
            msg = error
        else:
            msg = tb.format_exception_only(error)[-1].strip()

        return type(
                'obj', 
                (object,), 
                {'message': msg})

    def _get_status_template_record(self, fields, event):
        """(v1.0.0) Apply fix for borked splunklib.results.JSONResultsReader"""
        for field in fields:
            if field not in event.keys():
                event[field] = None
        return event


    def _verify_ko(self, ko_name, label, endpoint='configs/conf-', conf_name=None, must=False, must_not=False):
        """(v2.1.3)"""        
        if must and must_not:
            raise ValueError("The arguments 'must' and 'must_not' cannot both be set to True!")
        field = label.replace(' ', '_').lower()
        try:
            if endpoint == 'configs/conf-':
                target = f'{endpoint}{conf_name}/{ko_name}'
            else:
                target = f'{endpoint}/{ko_name}'
            stream = self.service.get(target, **self.ns)
            ko = spld.load(stream['body'].read()).feed.entry.content
        except HTTPError as e:
            if must:
                msg = f'''{e} -- [FATAL] Could not find a required {label}. \
                        Please ensure the {label} is accessible from the current app: \
                        {field}="{ko_name}"'''
                self.error_exit(error=self.__err(msg))
            return False
        except Exception as e:
            self.error_exit(error=self.__err(e))
        else:
            acl = ko.get('eai:acl')
            if must_not:
                msg = f'''[FATAL] The following {label} already exists! \
                        Please either 1) specify a different name, \
                        2) use the 'private="true"' option, \
                        3) modify the permissions for the existing {label}: or \
                        4) delete the existing {label}: \
                        {field}="{ko_name}", app="{acl.app}", \
                        owner="{acl.owner}", sharing="{acl.sharing}"'''
                self.error_exit(error=self.__err(msg))
            return ko


    def _verify_lookup_def(self, name, must=False, must_not=False):
        """(v2.1.1) Determine if the specified lookup definition is accessible."""
        return self._verify_ko(
                conf_name='transforms',
                ko_name=name,
                label='lookup definition',
                must=must, 
                must_not=must_not)
    
    def _verify_lookup_file(self, name, must=False, must_not=False):
        """(v2.1.1) Determine if the specified lookup file is accessible."""
        return self._verify_ko(
                endpoint='data/lookup-table-files',
                ko_name=name,
                label='lookup file',
                must=must, 
                must_not=must_not)
    
    def _verify_macro(self, name, must=False, must_not=False):
        """(v2.1.1) Determine if the specified macro is accessible."""
        return self._verify_ko(
                conf_name='macros',
                ko_name=name,
                label='macro',
                must=must, 
                must_not=must_not)
    

    def generate(self):
        
        # Check if user is authorized to run the command
        required_caps = ['omb_m2131_create_status_lookup']
        for cap in required_caps:
            if cap not in self.service.capabilities:
                msg = f'''PermissionError -- [FATAL] The user {self.metadata.searchinfo.owner} is not authorized to 
                        run this command. Please add the following capability: {cap}'''
                self.error_exit(error=self.__err(msg))

        
        os.environ['SPLUNK_HOME'] = os.environ.get('SPLUNK_HOME') or \
                self.service.settings.content.get(
                        'SPLUNK_HOME', 
                        os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
        
        
        # Variables
        LOOKUP_PDF = 'omb-m2131'
        LOOKUP_STATUS_PREFIX = 'omb-m2131-status'
        LOOKUP_STATUS_DELIM = '' if self.group in [None, 'None'] else '-'
        STATUS_FIELDS = [
            'check_id', 'm2131_lookup_version', 'm2131_lookup_version-compatibility', 
            'coverage-group_label', 'check-is_relevant', 'check-notes', 
            'coverage-data_collection_status', 'coverage-data_exists_elsewhere', 
            'coverage-data_in_siem', 'coverage-notes', 'coverage-point_of_contact', 
            'query', 'query-example_output', 'query-is_example', 'query-needs_review', 
            'query-notes', 'query-too_general']
        MACRO_ALL_GROUPS = 'omb-m2131-status-all'
        group_label = '' if self.group in [None, 'None'] else self.group.strip() 
        lookup_suffix = re.sub(r'[^\da-zA-Z\-]+', '_', group_label.lower())        
        lookup_def = f'{LOOKUP_STATUS_PREFIX}{LOOKUP_STATUS_DELIM}{lookup_suffix}'
        lookup_filename = f'{lookup_def}.csv'


        self.ns = {
            'owner': self.metadata.searchinfo.owner, 
            'app': self.metadata.searchinfo.app, 
            'sharing': 'user'
        }

        if not self.private:
            self.ns['sharing'] = 'app'


        props = {
            'batch_index_query': 0,
            'case_sensitive_match': 0,
            'filename': lookup_filename
        }
        

        query_get_status_template = f'''
            | inputlookup {LOOKUP_PDF}
            | fields check_id, m2131_lookup_version
            | eval coverage-group_label = "{group_label}" 
            | table {', '.join(STATUS_FIELDS)}
            '''
        query_write_status_template = f'''{query_get_status_template}
            | outputlookup create_context={self.ns.get('sharing')} {lookup_filename}
            '''
        # /Variables

        
        if self.preview:
            msg = f'''PREVIEW MODE ENABLED - Knowledge objects will NOT be created - \
                Lookup Definition=\"{lookup_def}\", \
                Lookup Filename=\"{lookup_filename}\", \
                App=\"{self.ns.get('app')}\", \
                Sharing=\"{self.ns.get('sharing')}\", \
                Owner=\"{self.ns.get('owner')}\"
            '''
            self.write_warning(msg)
            try:
                results = self.service.search(query_get_status_template)
            except Exception as e:
                self.error_exit(error=self.__err(e))
            else:
                # Sleep until done
                while not results.is_done():
                    sleep(.2)
                
                # Generate lookup file contents
                json_results = (self._get_status_template_record(STATUS_FIELDS, j) for j in \
                        splr.JSONResultsReader(results.results(output_mode='json', count=0)) \
                        if isinstance(j, dict))
                
                for event in json_results:
                        yield event

        else:
            
            # Pre-flight checks
            
            resp = self._verify_lookup_def(name=LOOKUP_PDF, must=True)
            resp = self._verify_lookup_def(name=lookup_def, must_not=True)
            resp = self._verify_lookup_file(name=lookup_filename, must_not=True)

            # /Pre-flight checks
            
            try:
                # Create lookup file
                self.service.search(query_write_status_template)
            except Exception as e:
                self.error_exit(error=self.__err(e))
            else:
                try:
                    # Create lookup definition
                    self.service.confs['transforms'].create(
                            lookup_def, 
                            **self.ns, 
                            **props)
                except Exception as e:
                    self.error_exit(error=self.__err(e))
                else:
                    
                    # Create/update macro if user is tracking a group
                    if len(group_label) > 0:
                        macro = self._verify_macro(name=MACRO_ALL_GROUPS)
                        macro_action = 'Update'
                        macro_result = 'Skipped'

                        if self.ns.get('sharing') != 'user':
                            macro_result = 'Success'
                            if not macro:
                                macro_action = 'Create'
                                props = {
                                    'definition': lookup_def
                                }


                                try:
                                    # Create macro
                                    self.service.confs['macros'].create(
                                        name=MACRO_ALL_GROUPS,
                                        **self.ns,
                                        **props
                                    )
                                except Exception as e:
                                    self.write_warning(self.__err(e).message)
                                    macro_result = 'Failed'
                            else:
                                '''
                                TODO: 
                                1) What if there's more than one due to one
                                being a private, cloned version and the other
                                being shared at app level?
                                A) For now, assume there's only one. If 
                                there is more than one, then assume someone
                                didn't rtfm or is trying to do something 
                                specific for their use case. There is no
                                perfect version 1. That's what midnight
                                hot patches are for.
                                '''
                                props = {
                                    'definition': f'{macro.definition}, {lookup_def}'
                                }
                                try:
                                    # Update macro
                                    resp = self.service.confs['macros'].post(
                                            path_segment=MACRO_ALL_GROUPS,
                                            **self.ns,
                                            **props)
                                except Exception as e:
                                    self.write_warning(self.__err(e).message)
                                    macro_result = 'Failed'


                    template = lambda w,x,y='Create',z='Success': {
                            'object': w,
                            'type': x,
                            'app': self.ns.get('app'),
                            'owner': self.ns.get('owner'),
                            'sharing': self.ns.get('sharing'),
                            'action': y,
                            'result': z
                        }
                    
                    results = [
                        template(lookup_def, "Lookup Definition"),
                        template(lookup_filename, "Lookup File")
                    ]

                    # Add notification if user is tracking a group
                    if len(group_label) > 0:
                        results.append(template(
                                MACRO_ALL_GROUPS, 
                                "Macro", 
                                macro_action, 
                                macro_result))

                    for event in results:
                        yield event


dispatch(M2131GenStatusCommand, sys.argv, sys.stdin, sys.stdout, __name__)
