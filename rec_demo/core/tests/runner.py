# import logging
#
# from django.test.runner import DiscoverRunner
# from rolepermissions.roles import assign_role
#
# from alpha_clinic.clinics.models import Clinic, ClinicMembership, ClinicMember
# from alpha_clinic.clinics.tests.factories import ClinicFactory, PhysicianFactory, NonMemberPhysicianFactory, \
#     CareTakingFacilityFactory
# from alpha_clinic.users.tests.factories import SimpleUserFactory
#
# logger = logging.getLogger(__name__)
#
#
# class EMRDiscoverRunner(DiscoverRunner):
#
#     def setup_databases(self, **kwargs):
#         logger.debug('SETTING UP DATABASE')
#         setup_result = super().setup_databases(**kwargs)
#         try:
#             physician_user = SimpleUserFactory(username='bones')
#         except Exception as e:
#             logger.error('COULD NOT create bones user ' + str(e))
#             raise e
#
#         clinic = ClinicFactory.create(name='Star Trek Clinic', owner=physician_user)
#         try:
#             self._create_bones(clinic, physician_user)
#         except Exception as e:
#             logger.error('COULD NOT create bones phyisian ' + str(e))
#             raise e
#
#         try:
#             self._create_cchapel(clinic)
#         except Exception as e:
#             logger.error('COULD NOT create cchapel assistant ' + str(e))
#             raise e
#
#         CareTakingFacilityFactory.create(name='Federation of Planets Hospital')
#
#         logger.debug('OUT SETUP DATABASE')
#         return setup_result
#
#     def _create_cchapel(self, clinic):
#         assistant_user = SimpleUserFactory(username='cchapel')
#         cchapel_exists = ClinicMember.objects.filter(user=assistant_user).count() == 1
#         if not cchapel_exists:
#             assistant_data = dict()
#             assistant_data['user'] = assistant_user
#             assistant_data['first_name'] = 'Cristine'
#             assistant_data['last_name'] = 'Chapel'
#             assistant_data['role'] = ClinicMember.ASSISTANT_ROLE
#             assistant = NonMemberPhysicianFactory.create(**assistant_data)
#             assign_role(assistant_user, 'assistant')
#             clinic.add_member(assistant)
#
#     def _create_bones(self, clinic, physician_user):
#         bones_exists = ClinicMember.objects.filter(user=physician_user).count() == 1
#         if not bones_exists:
#             physician_data = dict()
#             # physician_data['clinic'] = clinic
#             physician_data['user'] = physician_user
#             physician_data['first_name'] = 'Leonard'
#             physician_data['last_name'] = 'McCoy'
#             physician_data['middle_name'] = 'Horatio'
#             physician = NonMemberPhysicianFactory.create(**physician_data)
#             assign_role(physician_user, 'physician')
#             clinic.add_member(physician)
#
#     def teardown_databases(self, old_config, **kwargs):
#         logger.debug('TEARING DOWN DATABASE')
#         super().teardown_databases(old_config, **kwargs)
