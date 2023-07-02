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

from app.adecty_design.interfaces.tags.tags_parameters.unit.tag_parameter_delete import interface_tag_parameter_delete
from app.database.models import TagParameter
from app.decorators.admin_get import admin_get


blueprint_tag_parameter_delete = Blueprint(
    name='blueprint_tag_delete',
    import_name=__name__,
    url_prefix='/delete'
)


@blueprint_tag_parameter_delete.route(rule='/', endpoint='delete', methods=['GET', 'POST'])
@admin_get(not_return=True)
def tag_parameter_delete(tag_parameter_id: int):
    tag = TagParameter.get_by_id(tag_parameter_id)
    interface = interface_tag_parameter_delete(tag=tag)
    return interface
