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

from app.blueprints.products.create import blueprint_products_create
from app.blueprints.products.get import blueprint_products_get
from app.blueprints.products.unit import blueprint_product

blueprint_products = Blueprint(
    name='blueprint_products',
    import_name=__name__,
    url_prefix='/products',
)

blueprint_products.register_blueprint(blueprint=blueprint_products_get)
blueprint_products.register_blueprint(blueprint=blueprint_products_create)
blueprint_products.register_blueprint(blueprint=blueprint_product)
