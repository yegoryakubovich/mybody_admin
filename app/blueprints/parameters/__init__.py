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


from app.blueprints.parameters.create import blueprint_parameters_create
from app.blueprints.parameters.get import blueprint_parameters_get
from app.blueprints.parameters.unit import blueprint_parameter

blueprint_parameters = Blueprint(
    name='blueprint_parameters',
    import_name=__name__,
    url_prefix='/parameters',
)

blueprint_parameters.register_blueprint(blueprint=blueprint_parameters_get)
blueprint_parameters.register_blueprint(blueprint=blueprint_parameters_create)
blueprint_parameters.register_blueprint(blueprint=blueprint_parameter)
