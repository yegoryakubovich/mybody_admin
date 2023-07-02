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


from collections import defaultdict
from datetime import datetime, timedelta

from adecty_design.widgets.input import InputCheckbox
from flask import Blueprint, request, redirect

from app.adecty_design.interfaces import interface
from adecty_design.properties import Font, Margin, Align, AlignType
from adecty_design.widgets import Text, Button, ButtonType, Card, View, ViewType, Form, InputSelect, InputText, \
    InputButton

from app.blueprints.accounts.foods_cards.food_card import blueprint_food_card
from app.database.models import OrderEating, Product, Account, Admin, TimeFood
from app.decorators.admin_get import admin_get


blueprint_foods_cards = Blueprint(
    name='blueprint_foods_cards',
    import_name=__name__,
    url_prefix='/<int:account_id>/foods_cards'
)

blueprint_foods_cards.register_blueprint(blueprint=blueprint_food_card)


@blueprint_foods_cards.route(rule='/', endpoint='get', methods=['GET'])
@admin_get()
def foods_get(account_id, admin: Admin):
    foods = OrderEating.select().where(OrderEating.datetime)
    account = Account.get_by_id(admin.account_id)
    foods_by_date = defaultdict(list)
    for food in foods:
        foods_by_date[food.datetime.date()].append(food)

    widgets = [
        View(
            properties_additional=[Align(type=AlignType.space_between)],
            type=ViewType.horizontal,
            widgets=[
                Text(
                    text='Карта питания',
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                    margin=Margin(down=16),
                ),
                Button(
                    type=ButtonType.chip,
                    text='Создать',
                    url=f'/accounts/{account_id}/foods_cards/create'
                ),
            ]
        )
    ]

    foods_by_date = defaultdict(list)

    for food in foods:
        foods_by_date[food.datetime.date()].append(food)

    for date, foods_in_date in foods_by_date.items():
        card_content = []
        card_content.append(Text(
            text=f'Дата: {date}',
            font=Font(
                size=17,
                weight=700
            ),
            margin=Margin(down=8)
        ))

        time_food_ids = set()
        for food in foods_in_date:
            time_food_id = food.time_food_id
            if time_food_id not in time_food_ids:
                time_food_ids.add(time_food_id)
                card_content.append(Text(text=f'{food.time_food.name.value_get(account)}'))
            card_content.append(Text(text=f'{food.name.product_name_get(account)} - {food.unit}'))

        buttons = [
            Button(
                type=ButtonType.chip,
                text='Редактировать',
                url=f'/accounts/{account_id}/foods_cards/{date}/update',
            ),
            Button(
                type=ButtonType.chip,
                text='Удалить',
                url=f'/accounts/{account_id}/foods_cards/{date}/unit'
            )
        ]
        button_view = View(
            widgets=buttons,
            type=ViewType.horizontal,
            margin=Margin(horizontal=8, right=6)
        )
        card_content.append(button_view)

        widgets.append(Card(
            widgets=card_content,
            margin=Margin(down=12),
        ))

    interface_html = interface.html_get(
        widgets=widgets,
        active='accounts',
    )

    return interface_html


@blueprint_foods_cards.route(rule='/create', endpoint='create', methods=['GET', 'POST'])
@admin_get()
def foods_create(account_id, admin: Admin):
    if request.method == 'POST':
        unit = request.form.get('unit')
        product = request.form.get('product')
        product = Product().get_by_product(name=product, account=admin.account)
        unit_type = request.form.get('unit_type')
        time_food = request.form.get('time_food')
        food = TimeFood().get_by_food(name=time_food, account=admin.account)
        account = Account.get_or_none(Account.id == account_id)

        selected_dates = []
        for date_checkbox in request.form:
            if date_checkbox.startswith('date_'):
                date_str = date_checkbox[5:]
                selected_dates.append(datetime.strptime(date_str, '%Y-%m-%d'))

        orders = []
        for date in selected_dates:
            order = OrderEating(account=account, name=product, time_food=food, unit="{} {}".format(unit, unit_type),
                                datetime=date)
            orders.append(order)

        for order in orders:
            order.save()

        return redirect(f'/accounts/{account_id}/foods_cards/create')

    products = Product.select()
    product_options = [product.product_name_get(account=admin.account) for product in products] if products else None
    times_foods = TimeFood.select()
    food_options = [time_food.food_name_get(account=admin.account) for time_food in times_foods]\
        if times_foods else None

    if not products or not times_foods:
        error_message = "Сначала необходимо создать категорию и приём пищи."
        widgets = [
            Text(
                text=error_message,
                font=Font(
                    size=16,
                    weight=700,
                ),
                margin=Margin(down=16),
            ),
        ]
        interface_html = interface.html_get(
            widgets=widgets,
            active='accounts',
        )
        return interface_html

    now = datetime.now()
    dates = [now + timedelta(days=i) for i in range(14)]

    date_checkboxes = [InputCheckbox(id='date_{}'.format(date.strftime('%Y-%m-%d')), label=date.strftime('%Y-%m-%d'))
                       for date in dates]

    unit_options = ['грамм', 'штук']

    widgets = [
        Text(
            text='Создание карты',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='Даты',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                *date_checkboxes,
                Text(
                    text='Время приёма пищи',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputSelect(id='time_food', options=food_options, selected=food_options),
                Text(
                    text='Продукт',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputSelect(id='product', options=product_options, selected=product_options),
                Text(
                    text='Единицы измерения',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputSelect(id='unit_type', options=unit_options, selected=unit_options[0]),
                Text(
                    text='Количество',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputText(id='unit'),
                InputButton(text='Сохранить', margin=Margin(horizontal=8)),
            ],
        ),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='accounts',
    )

    return interface_html
