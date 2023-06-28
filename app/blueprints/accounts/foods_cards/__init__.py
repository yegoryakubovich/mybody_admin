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


from datetime import datetime, timedelta

from adecty_design.widgets.input import InputCheckbox
from flask import Blueprint, request, redirect

from app.adecty_design.interface import interface
from adecty_design.properties import Font, Margin, Align, AlignType
from adecty_design.widgets import Text, Button, ButtonType, Card, View, ViewType, Form, InputSelect, InputText, \
    InputButton
from app.database.models import OrderEating, Product, Article, Account, Admin, TimeFood
from app.decorators.admin_get import admin_get
from app.database import Text as TextDB


blueprint_foods_cards = Blueprint(
    name='blueprint_foods_cards',
    import_name=__name__,
    url_prefix='/<int:account_id>/foods_cards'
)


@blueprint_foods_cards.route(rule='/', endpoint='get', methods=['GET'])
@admin_get(not_return=True)
def foods_get(account_id):
    today = datetime.now().strftime("%Y-%m-%d")
    foods = OrderEating.select().where(OrderEating.datetime.startswith(today))
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

    buttons_view = None
    current_time_food = None
    for food in foods:
        if food.time_food != current_time_food:
            if buttons_view is not None:
                widgets.append(buttons_view)

            current_time_food = food.time_food
            widgets.append(
                Text(text=f'Дата: {food.datetime.date()}')
            )
            widgets.append(
                Text(text=f'Приём пищи: {current_time_food.name}')
            )

        widgets.append(
            Text(text=f'Название продукта: {food.name}')
        )
        widgets.append(
            Text(text=f'Количество: {food.unit}')
        )

        buttons_view = View(
            type=ViewType.horizontal,
            widgets=[
                Button(
                    type=ButtonType.chip,
                    text='Редактировать',
                    margin=Margin(horizontal=8, right=6),
                    url=f'/accounts/{account_id}/foods_cards/update/{food.id}',
                ),
                Button(
                    type=ButtonType.chip,
                    text='Удалить',
                    margin=Margin(horizontal=8, right=6),
                    url=f'/accounts/{account_id}/foods_cards/delete/{food.id}',
                ),
            ]
        )

    if buttons_view:
        widgets.append(buttons_view)

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
        name = request.form.get('name')
        unit_type = request.form.get('unit_type')
        time_food = request.form.get('time_food')
        food = TimeFood().get_by_food(name=time_food, account=admin.account)
        article_name = request.form.get('article_name')
        article = Article().get_by_aricle(name=article_name, account=admin.account)
        account = Account.get_or_none(Account.id == account_id)
        text = TextDB()
        text.save()
        text.default_create(value=name)

        selected_dates = []
        for date_checkbox in request.form:
            if date_checkbox.startswith('date_'):
                date_str = date_checkbox[5:]
                selected_dates.append(datetime.strptime(date_str, '%d-%m-%Y'))

        orders = []
        for date in selected_dates:
            order = OrderEating(account=account, name=text, time_food=food, unit="{} {}".format(unit, unit_type),
                                article=article, datetime=date)
            orders.append(order)

        for order in orders:
            order.save()

        return redirect(f'/accounts/{account_id}/foods_cards/create')

    products = Product.select()
    product_options = [product.product_name_get(account=admin.account) for product in products] if products else None
    articles = Article.select()
    article_options = [article.article_name_get(account=admin.account) for article in articles] if articles else None
    times_foods = TimeFood.select()
    food_options = [time_food.food_name_get(account=admin.account) for time_food in times_foods] if times_foods \
        else None

    if not products or not articles or not times_foods:
        error_message = "Сначала необходимо создать категорию, статью и приём пищи."
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

    date_checkboxes = [InputCheckbox(id='date_{}'.format(date.strftime('%d-%m-%Y')), label=date.strftime('%d-%m-%Y'))
                       for date in dates]

    unit_options = ['Граммы', 'Штук']

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
                InputSelect(id='name', options=product_options, selected=product_options),
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
                Text(
                    text='Статья',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputSelect(id='article_name', options=article_options, selected=article_options),
                InputButton(text='Сохранить', margin=Margin(horizontal=8)),
            ],
        ),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='accounts',
    )

    return interface_html