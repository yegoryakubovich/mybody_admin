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


from flask import Blueprint, redirect

from app.blueprints.account import blueprint_account
from app.blueprints.articles import blueprint_articles
from app.blueprints.errors import blueprint_errors
from app.blueprints.languages import blueprint_languages
from app.blueprints.items import blueprint_items
from app.decorators.admin_get import admin_get


blueprint_main = Blueprint(
    name='blueprint_account',
    import_name=__name__,
)


blueprint_main.register_blueprint(blueprint=blueprint_errors)
blueprint_main.register_blueprint(blueprint=blueprint_account)
blueprint_main.register_blueprint(blueprint=blueprint_items)
blueprint_main.register_blueprint(blueprint=blueprint_languages)


@blueprint_main.route('/', methods=['GET'])
@admin_get(not_return=True)
def main():
    return redirect('/items')
