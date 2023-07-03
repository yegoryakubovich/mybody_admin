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


from adecty_design.properties import Font, Margin, Padding
from adecty_design.widgets import Text, Card, Dictionary, View, ViewType, Button, ButtonType

from app.adecty_design.colors import colors
from app.adecty_design.functions.icon_get import icon_get
from app.adecty_design.widgets.unit import Unit


class ModelsViewerTypes:
    cards = 'cards'


def models_viewer_get(type: str = ModelsViewerTypes.cards, units: list[Unit] = None):
    widgets = []
    if not units:
        widgets += [
            Text(
                text='У вас нет готовых моделей',
                font=Font(size=18),
                margin=Margin(horizontal=12),
            ),
        ]
        return widgets

    for unit in units:
        if type == ModelsViewerTypes.cards:
            card = Card(
                widgets=[],
                margin=Margin(horizontal=12),
                padding=Padding(vertical=24, horizontal=18),
            )

            if unit.name:
                card.widgets += [
                    Text(
                        text=unit.name,
                        font=Font(
                            weight=600,
                            size=22,
                        ),
                    ),
                ]
            if unit.parameters:
                card.widgets += [
                    Dictionary(
                        keys=[Text(text=key) for key in unit.parameters.keys()],
                        values=[Text(text=value) for value in unit.parameters.values()],
                        margin=Margin(horizontal=12),
                    ),
                ]
            if unit.actions:
                card.widgets += [
                    View(
                        type=ViewType.horizontal,
                        widgets=[
                            Button(
                                type=ButtonType.chip,
                                text=action.name,
                                url=action.url,
                                icon=icon_get(filename=action.icon, color=colors.text),
                                color_background=colors.background_secondary,
                                margin=Margin(right=8),
                            )
                            for action in unit.actions
                        ],
                    ),
                ]

            widgets.append(card)

    return widgets
