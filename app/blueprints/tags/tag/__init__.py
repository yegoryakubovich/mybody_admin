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

from app.adecty_design.interface import interface
from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, InputButton, InputText, Form

from app.database.models import Admin, TagParameter
from app.decorators.admin_get import admin_get
from app.database import Text as TextDB


blueprint_tag = Blueprint(
    name='blueprint_tag',
    import_name=__name__,
    url_prefix='/<int:tag_id>/'
)


@blueprint_tag.route(rule='/delete', endpoint='delete', methods=['GET', 'POST'])
@admin_get(not_return=True)
def tag_delete(tag_id: int):
    try:
        tag = TagParameter.get_by_id(tag_id)
    except DoesNotExist:
        return redirect('/tags')

    tag.delete_instance()
    return redirect('/tags')


@blueprint_tag.route(rule='/edit', endpoint='edit', methods=['GET', 'POST'])
@admin_get()
def tag_edit(admin: Admin, tag_id: int):
    try:
        tag = TagParameter.get_by_id(tag_id)
    except DoesNotExist:
        return redirect('/tags')

    if request.method == 'POST':
        name_value = request.form.get('name_value')

        text = TextDB()
        text.save()
        text.default_create(value=name_value)

        tag.name = text
        tag.save()

        return redirect('/tags')

    widgets = [
        Text(
            text='Редактирование тега',
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
                InputText(id='name_value', value=tag.name.value_get(admin.account)),
                InputButton(text='Сохранить', margin=Margin(horizontal=8)),
            ],
        ),
    ]

    interface_html = interface.html_get(widgets=widgets)
    return interface_html
