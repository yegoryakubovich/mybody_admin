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
from adecty_design.properties import Font, Margin
from adecty_design.widgets import InputSelect, InputText, InputButton, Form, Text, Card
from flask import Blueprint, redirect, request

from app.adecty_design.interfaces import interface
from app.database.models import OrderEating, Product, TimeFood, Admin
from app.decorators.admin_get import admin_get


blueprint_food_card = Blueprint(
    name='blueprint_food_card',
    import_name=__name__,
    url_prefix='/<string:date>'
)


@blueprint_food_card.route(rule='/unit', endpoint='unit', methods=['GET', 'POST'])
@admin_get(not_return=True)
def food_card_delete(account_id, date):
    food_cards = OrderEating.select().where((OrderEating.account_id == account_id) &
                                            (OrderEating.datetime.startswith(date)))
    for food_card in food_cards:
        food_card.delete_instance()

    return redirect(f'/accounts/{account_id}/foods_cards')


@blueprint_food_card.route(rule='/update', endpoint='update', methods=['GET', 'POST'])
@admin_get()
def food_card_update(account_id, date, admin: Admin):
    food_cards = OrderEating.select().where((OrderEating.account_id == account_id) &
                                            (OrderEating.datetime.startswith(date)))
    if request.method == 'POST':
        # Обработка данных из формы редактирования
        for food_card in food_cards:
            unit = request.form.get(f'unit_{food_card.id}')
            product = request.form.get(f'product_{food_card.id}')
            product = Product().get_by_product(name=product, account=admin.account)
            unit_type = request.form.get(f'unit_type_{food_card.id}')
            time_food = request.form.get(f'time_food_{food_card.id}')
            food = TimeFood().get_by_food(name=time_food, account=admin.account)

            # Обновление данных карточки питания
            food_card.unit = "{} {}".format(unit, unit_type)
            food_card.name = product
            food_card.time_food = food
            food_card.save()

        return redirect(f'/accounts/{account_id}/foods_cards')

    products = Product.select()
    product_options = [product.product_name_get(account=admin.account) for product in products]
    times_foods = TimeFood.select()
    food_options = [time_food.food_name_get(account=admin.account) for time_food in times_foods]
    unit_options = ['грамм', 'штук']

    widgets = [
        Text(
            text=f'Редактирование карточки {date}',
            font=Font(size=32, weight=700),
            margin=Margin(down=16),
        ),
    ]

    form_widgets = []

    for food_card in food_cards:
        card_widgets = [
            Text(
                text='Время приёма пищи',
                font=Font(
                    size=14,
                    weight=700,
                ),
            ),
            InputSelect(
                id=f'time_food_{food_card.id}',
                options=food_options,
                selected=food_card.time_food.food_name_get(account=admin.account),
            ),
            Text(
                text='Продукт',
                font=Font(
                    size=14,
                    weight=700,
                ),
            ),
            InputSelect(
                id=f'product_{food_card.id}',
                options=product_options,
                selected=food_card.name.product_name_get(account=admin.account),
            ),
            Text(
                text='Единицы измерения',
                font=Font(
                    size=14,
                    weight=700,
                ),
            ),
            InputSelect(
                id=f'unit_type_{food_card.id}',
                options=unit_options,
                selected=food_card.unit.split(' ')[1],
            ),
            Text(
                text='Количество',
                font=Font(
                    size=14,
                    weight=700,
                ),
            ),
            InputText(
                id=f'unit_{food_card.id}',
                value=food_card.unit.split(' ')[0],
            ),
        ]

        card = Card(widgets=card_widgets,
                    margin=Margin(down=12))
        form_widgets.append(card)

    form_widgets.append(InputButton(text='Сохранить', margin=Margin(horizontal=8)))
    form = Form(widgets=form_widgets)
    widgets.append(form)

    interface_html = interface.html_get(
        widgets=widgets,
        active='accounts',
    )

    return interface_html
