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


from app.adecty_design.interfaces.products.get import interface_products_get
from app.database import Admin
from app.decorators.admin_get import admin_get


blueprint_products_get = Blueprint(
    name='blueprint_products_get',
    import_name=__name__,
    url_prefix='/',
)


@blueprint_products_get.route(rule='/', endpoint='get', methods=['GET', 'POST'])
@admin_get()
def products_get(admin: Admin):
    interface = interface_products_get(admin)
    return interface, 200
