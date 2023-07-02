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


from flask import Blueprint, request, redirect

from app.adecty_design.interfaces import interface
from adecty_design.properties import Font, Margin, Align, AlignType
from adecty_design.widgets import Text, Button, ButtonType, Card, View, ViewType, Form, InputText, InputButton

from app.adecty_design.interfaces.tags.tags_parameters.get import interface_tegs_parameters_get
from app.blueprints.tags.tags_parameters.unit import blueprint_tag_parameter
from app.database.models import Admin, TagParameter
from app.decorators.admin_get import admin_get
from app.database import Text as TextDB


blueprint_tags_parameters = Blueprint(
    name='blueprint_tags_parameters',
    import_name=__name__,
    url_prefix='/tags_parameters'
)

blueprint_tags_parameters.register_blueprint(blueprint=blueprint_tag_parameter)


@blueprint_tags_parameters.route(rule='/', endpoint='get', methods=['GET'])
@admin_get()
def tags_parameters_get():
    interface = interface_tegs_parameters_get()
    return interface


@blueprint_tags_parameters.route(rule='/create', endpoint='create', methods=['GET', 'POST'])
@admin_get(not_return=True)
def tags_create():
    if request.method == 'POST':
        tags_value = request.form.get('tags_value')

        text = TextDB()
        text.save()
        text.default_create(value=tags_value)

        tag = TagParameter(name=text)
        tag.save()

        return redirect('/tags')

    widgets = [
        Text(
            text='Создание тега',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='Название',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputText(id='tags_value'),
                InputButton(text='Сохранить', margin=Margin(horizontal=8)),
            ],
        ),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='tags',
    )
    return interface_html
