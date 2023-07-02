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
from adecty_design.widgets import Text, Button, ButtonType, Card, View, ViewType, InputButton, InputSelect, InputText, \
    Form

from app.blueprints.parameters.parameter import blueprint_parameter
from app.database.models import Admin, Parameter, TagParameter
from app.decorators.admin_get import admin_get
from app.database import Text as TextDB


blueprint_parameters = Blueprint(
    name='blueprint_parameters',
    import_name=__name__,
    url_prefix='/parameters'
)

blueprint_parameters.register_blueprint(blueprint=blueprint_parameter)


@blueprint_parameters.route(rule='/', endpoint='get', methods=['GET'])
@admin_get()
def parameters(admin: Admin):
    widgets = [
        View(
            properties_additional=[Align(type=AlignType.space_between)],
            type=ViewType.horizontal,
            widgets=[
                Text(
                    text='Список вопросов ',
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                    margin=Margin(down=16),
                ),
                Button(
                    type=ButtonType.chip,
                    text='Создать',
                    url='/parameters/create'
                ),
            ]
        )
    ]

    for parameter in Parameter.select():
        parameter_text = parameter.text.value_get(admin.account)
        new_widget = Card(
            margin=Margin(down=16),
            widgets=[
                Text(text=f"Вопрос: {parameter_text}", font=Font(size=16)),
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/parameters/{parameter.id}/edit',
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Удалить',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/parameters/{parameter.id}/delete',
                        ),
                    ],
                ),
            ]
        )
        widgets.append(new_widget)

    interface_html = interface.html_get(
        widgets=widgets,
        active='parameters',
    )
    return interface_html


@blueprint_parameters.route(rule='/create', endpoint='create', methods=['GET', 'POST'])
@admin_get()
def parameters_create(admin: Admin):
    if request.method == 'POST':
        key_parameter = request.form.get('key_parameter')
        is_gender = request.form.get('is_gender')
        text_value = request.form.get('text_value')
        tag_name = request.form.get('tag_name')
        tag_parameter = TagParameter().get_by_name(name=tag_name, account=admin.account)

        text = TextDB()
        text.save()
        text.default_create(value=text_value)

        if is_gender == 'Мужской':
            is_gender = 'men'
        elif is_gender == 'Женский':
            is_gender = 'female'
        else:
            is_gender = None

        parameter = Parameter(text=text, is_gender=is_gender, key_parameter=key_parameter, tag=tag_parameter)
        parameter.save()

        return redirect('/parameters')

    options_gender = ['Оба', 'Мужской', 'Женский']
    tag_parameters = TagParameter.select()
    options_tag = [tag.name_get(account=admin.account) for tag in tag_parameters]

    if not options_tag:
        widgets = [
            Text(
                text='Для начала необходимо создать тег',
                font=Font(
                    size=16,
                    weight=700,
                ),
                margin=Margin(down=16),
            ),
            Button(
                type=ButtonType.default,
                text='Создать тег',
                url='/tags/create',
                margin=Margin(down=8),
            ),
        ]
    else:
        widgets = [
            Text(
                text='Создание вопроса',
                font=Font(
                    size=32,
                    weight=700,
                ),
                margin=Margin(down=16),
            ),
            Form(
                widgets=[
                    Text(
                        text='Ключ',
                        font=Font(
                            size=14,
                            weight=700,
                        ),
                    ),
                    InputText(id='key_parameter'),
                    Text(
                        text='Текст',
                        font=Font(
                            size=14,
                            weight=700,
                        ),
                    ),
                    InputText(id='text_value'),
                    Text(
                        text='Пол',
                        font=Font(
                            size=14,
                            weight=700,
                        ),
                    ),
                    InputSelect(id='is_gender', options=options_gender),
                    Text(
                        text='Тег',
                        font=Font(
                            size=14,
                            weight=700,
                        ),
                    ),
                    InputSelect(id='tag_name', options=options_tag),
                    InputButton(text='Сохранить', margin=Margin(horizontal=8)),
                ],
            ),
        ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='parameters',
    )
    return interface_html
