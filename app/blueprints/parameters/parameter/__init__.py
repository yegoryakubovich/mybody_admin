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
from peewee import DoesNotExist

from app.adecty_design.interfaces import interface
from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, InputButton, InputSelect, InputText, Form

from app.database.models import Admin, Parameter
from app.decorators.admin_get import admin_get
from app.database import Text as TextDB


blueprint_parameter = Blueprint(
    name='blueprint_parameter',
    import_name=__name__,
    url_prefix='/<int:parameter_id>/'
)


@blueprint_parameter.route(rule='/unit', endpoint='unit', methods=['GET', 'POST'])
@admin_get(not_return=True)
def parameters_delete(parameter_id: int):
    try:
        parameter = Parameter.get_by_id(parameter_id)
    except DoesNotExist:
        return redirect('/parameters')

    parameter.delete_instance()
    return redirect('/parameters')


@blueprint_parameter.route(rule='/edit', endpoint='edit', methods=['GET', 'POST'])
@admin_get()
def parameter_edit(admin: Admin, parameter_id: int):
    try:
        parameter = Parameter.get_by_id(parameter_id)
    except DoesNotExist:
        return redirect('/parameters')

    if request.method == 'POST':
        key_parameter = request.form.get('key_parameter')
        is_gender = request.form.get('is_gender')
        text_value = request.form.get('text_value')

        text = TextDB()
        text.save()
        text.default_create(value=text_value)

        if is_gender == 'Мужской':
            is_gender = 'men'
        elif is_gender == 'Женский':
            is_gender = 'female'
        else:
            is_gender = None

        parameter.text = text
        parameter.is_gender = is_gender
        parameter.key_parameter = key_parameter
        parameter.save()

        return redirect('/parameters')

    options = ['Оба', 'Мужской', 'Женский']

    widgets = [
        Text(
            text='Редактирование вопроса',
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
                InputText(id='key_parameter', value=parameter.key_parameter),
                Text(
                    text='Текст',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputText(id='text_value', value=parameter.text.value_get(admin.account)),
                Text(
                    text='Пол',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputSelect(id='is_gender', options=options, selected=parameter.is_gender),
                InputButton(text='Сохранить', margin=Margin(horizontal=8)),
            ],
        ),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='parameters',
    )
    return interface_html
