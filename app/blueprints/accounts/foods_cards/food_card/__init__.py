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


from flask import Blueprint, redirect

from app.database.models import OrderEating
from app.decorators.admin_get import admin_get


blueprint_food_card = Blueprint(
    name='blueprint_food_card',
    import_name=__name__,
    url_prefix='/<string:date>'
)


@blueprint_food_card.route(rule='/delete', endpoint='delete', methods=['GET', 'POST'])
@admin_get(not_return=True)
def food_card_delete(account_id, date):
    food_cards = OrderEating.select().where((OrderEating.account_id == account_id) &
                                            (OrderEating.datetime.startswith(date)))
    for food_card in food_cards:
        food_card.delete_instance()

    return redirect(f'/accounts/{account_id}/foods_cards')


'''@blueprint_food_card.route(rule='/update', endpoint='update', methods=['GET', 'POST'])
@admin_get()
def foods_update():
'''