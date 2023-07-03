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

from app.adecty_design.interfaces.languages.unit.language_update import interface_language_update
from app.database.models import Language
from app.decorators.admin_get import admin_get

blueprint_language_update = Blueprint(
    name='blueprint_language_update',
    import_name=__name__,
    url_prefix='/update'
)


@blueprint_language_update.route(rule='/', endpoint='update', methods=['GET', 'POST'])
@admin_get(not_return=True)
def language_update(language_id):
    language = Language.get_by_id(language_id)
    interface = interface_language_update(language=language)
    return interface
