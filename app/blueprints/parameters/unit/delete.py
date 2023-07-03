#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from flask import Blueprint


from app.adecty_design.interfaces.parameters.unit.parameter_delete import interface_parameter_delete
from app.database.models import Parameter
from app.decorators.admin_get import admin_get

blueprint_parameter_delete = Blueprint(
    name='blueprint_parameter_delete',
    import_name=__name__,
    url_prefix='/delete'
)


@blueprint_parameter_delete.route(rule='/', endpoint='delete', methods=['GET', 'POST'])
@admin_get(not_return=True)
def parameter_delete(parameter_id):
    parameter = Parameter.get_by_id(parameter_id)
    interface = interface_parameter_delete(parameter=parameter)
    return interface
