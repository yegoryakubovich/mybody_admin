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

from app.adecty_design.interface import interface
from adecty_design.properties import Font, Margin, Align, AlignType
from adecty_design.widgets import Text, Button, ButtonType, Card, View, ViewType
from app.database.models import OrderEating
from app.decorators.admin_get import admin_get


blueprint_foods_cards = Blueprint(
    name='blueprint_foods_cards',
    import_name=__name__,
    url_prefix='/<int:account_id>/foods_cards'
)


@blueprint_foods_cards.route(rule='/', endpoint='get', methods=['GET'])
@admin_get(not_return=True)
def foods_get(account_id):
    foods = OrderEating.select()
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

    for food in foods:
        new_widget = Card(
            margin=Margin(down=16),
            widgets=[
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/accounts/{account_id}/foods_cards/update',
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Удалить',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/accounts/{account_id}/foods_cards/delete',
                        ),
                    ],
                ),
                Text(
                    text=f"Название: {food.name}\n"
                         f"Количество: {food.unit}\n"
                         f"Статья: {food.article}",
                    font=Font(size=16)
                )
            ]
        )
        widgets.append(new_widget)

    interface_html = interface.html_get(
        widgets=widgets,
        active='accounts',
    )

    return interface_html


@blueprint_foods_cards.route(rule='/create', endpoint='create', methods=['GET'])
@admin_get(not_return=True)
def foods_create(account_id):
    widgets = [
        Card(
            widgets=[
                Button(
                    text='Добавить упражнение',
                    url=f'/foods_cards/exercise/create',
                    margin=Margin(down=8)
                ),
                Button(
                    text='Добавить статью',
                    url=f'/foods_cards/article/create',
                    margin=Margin(down=8)
                )
            ],
            margin=Margin(down=16)
        )
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='accounts',
    )

    return interface_html
