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


from adecty_design.properties import Margin, Font
from adecty_design.widgets import InputButton, Form, Text, Button, View, ViewType

from app.adecty_design.colors import colors


def model_deleter_get(url_back: str):
    widgets = [
        Form(
            widgets=[
                Text(
                    text='Вы уверены, что хотите удалить выбранную модель?',
                    font=Font(size=18),
                    margin=Margin(horizontal=12),
                ),
                View(
                    widgets=[
                        InputButton(
                            text='Да, удалить',
                            margin=Margin(
                                horizontal=0,
                                right=8,
                            ),
                        ),
                        Button(
                            text=Text(
                                text='Нет, вернуться',
                                font=Font(
                                    weight=700,
                                    color=colors.primary,
                                ),
                            ),
                            url=url_back,
                        ),
                    ],
                    type=ViewType.horizontal,
                    margin=Margin(top=12),
                ),
            ],
        ),
    ]

    return widgets
