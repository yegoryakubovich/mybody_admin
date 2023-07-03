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


from adecty_design.properties import Font, Align, AlignType, Margin
from adecty_design.widgets import View, ViewType, Text, Button, ButtonType

from app.adecty_design.colors import colors
from app.adecty_design.functions.icon_get import icon_get


def header_get(text: str, url_back: str = None, create_url: str = None):
    header_widgets = []

    if url_back:
        header_widgets += [
            Button(
                type=ButtonType.chip,
                url=url_back,
                color_background=colors.background,
                icon=icon_get(filename='back.svg', color=colors.text),
                margin=Margin(horizontal=0, vertical=0),
            ),
        ]

    header_widgets += [
        Text(
            text=text,
            font=Font(
                size=32,
                weight=700,
            ),
        ),
    ]

    if create_url:
        header_widgets += [
            Button(
                type=ButtonType.chip,
                text='Создать',
                url=create_url,
                icon=icon_get(filename='create.svg', color=colors.text),
            ),
        ]

    header = View(
        type=ViewType.horizontal,
        widgets=header_widgets,
        properties_additional=[Align(type=AlignType.space_between)] if create_url else [],
    )

    return header
