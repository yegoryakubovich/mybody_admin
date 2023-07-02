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
from adecty_design.widgets import Text, Button, ButtonType, Card, View, ViewType, InputButton, InputText, Form

from app.blueprints.products.product import blueprint_product
from app.blueprints.times_foods.time_food import blueprint_time_food
from app.database.models import Admin, TimeFood
from app.decorators.admin_get import admin_get
from app.database import Text as TextDB


blueprint_times_foods = Blueprint(
    name='blueprint_times_foods',
    import_name=__name__,
    url_prefix='/times_foods'
)

blueprint_times_foods.register_blueprint(blueprint=blueprint_time_food)


@blueprint_times_foods.route(rule='/', endpoint='get', methods=['GET'])
@admin_get()
def time_food_get(admin: Admin):
    widgets = [
        View(
            properties_additional=[Align(type=AlignType.space_between)],
            type=ViewType.horizontal,
            widgets=[
                Text(
                    text='Список приёмов пищи',
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                    margin=Margin(down=16),
                ),
                Button(
                    type=ButtonType.chip,
                    text='Создать',
                    url='/times_foods/create'
                ),
            ]
        )
    ]

    for food in TimeFood.select():
        food_text = food.name.value_get(admin.account)
        new_widget = Card(
            margin=Margin(down=16),
            widgets=[
                Text(text=f"Название приёма пиши: {food_text}", font=Font(size=16)),
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/times_foods/{food.id}/update',
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Удалить',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/times_foods/{food.id}/delete',
                        ),
                    ],
                ),
            ]
        )
        widgets.append(new_widget)

    interface_html = interface.html_get(
        widgets=widgets,
        active='times_foods',
    )

    return interface_html


@blueprint_times_foods.route(rule='/create', endpoint='create', methods=['GET', 'POST'])
@admin_get(not_return=True)
def time_food_create():
    if request.method == 'POST':
        name = request.form.get('name')

        text = TextDB()
        text.save()
        text.default_create(value=name)

        time_food = TimeFood(name=text)
        time_food.save()

        return redirect(f'/times_foods')

    widgets = [
        Text(
            text='Создание приёма пищи',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='Название приёма пищи',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputText(id='name'),
                InputButton(text='Сохранить', margin=Margin(horizontal=8)),
            ],
        ),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='products',
    )

    return interface_html
