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


from adecty_design.widgets.required import Navigation, NavigationItem
from app.functions.icon_get import icon_get


navigation_main = Navigation(
    items=[
        NavigationItem(
            id='items',
            name='Текста',
            url='/items',
            icon=icon_get(filename='items.svg'),
        ),
        NavigationItem(
            id='articles',
            name='Статьи',
            url='/articles',
            icon=icon_get(filename='items.svg'),
        ),
        NavigationItem(
            id='parameters',
            name='Анкета',
            url='/parameters',
            icon=icon_get(filename='items.svg'),
        ),
        NavigationItem(
            id='tags',
            name='Теги',
            url='/tags',
            icon=icon_get(filename='items.svg'),
        ),
        NavigationItem(
            id='languages',
            name='Языки',
            url='/languages',
            icon=icon_get(filename='items.svg'),
        )
    ],
)
navigation_none = Navigation(
    items=[],
)
