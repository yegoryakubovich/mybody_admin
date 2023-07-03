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
from app.database.models import Admin, Account, TimeFood
from app.decorators.admin_get import admin_get
from app.database import Text as TextDB


blueprint_time_food = Blueprint(
    name='blueprint_time_food',
    import_name=__name__,
    url_prefix='/<int:food_id>'
)


@blueprint_time_food.route(rule='/unit', endpoint='unit', methods=['GET', 'POST'])
@admin_get(not_return=True)
def time_food_delete(food_id):
    try:
        food = TimeFood.get(TimeFood.id == food_id)
    except DoesNotExist:
        return redirect('/times_foods')

    food.delete_instance()

    return redirect('/times_foods')


@blueprint_time_food.route(rule='/update', endpoint='update', methods=['GET', 'POST'])
@admin_get()
def time_food_update(food_id: int, admin: Admin):
    food = TimeFood.get_by_id(food_id)
    account = Account.get_by_id(admin.account_id)
    text_id = food.name.id
    text = TextDB.get_or_none(TextDB.id == text_id)

    if request.method == 'POST':
        name = request.form['name']
        if text:
            text.value_set(account, name)
        else:
            new_text = TextDB()
            new_text.save()
            new_text.default_create(value=name)

        return redirect('/times_foods')

    text_db = TextDB.get_or_none(TextDB.id == text_id)
    text = text_db.value_get(account)
    widgets = [
        Text(
            text='Редактирование продукта',
            font=Font(size=32, weight=700),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='Название приёма пиши',
                    font=Font(size=14, weight=700),
                ),
                InputText(id='name', value=text),
                InputButton(text='Сохранить', margin=Margin(top=8)),
            ],
        ),
    ]
    interface_html = interface.html_get(
        widgets=widgets,
        active='times_foods',
    )

    return interface_html
