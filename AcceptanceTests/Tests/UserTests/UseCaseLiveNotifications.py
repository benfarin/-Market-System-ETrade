import datetime
import os
import pytest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from notificationsApp.consumers import NotificationsConsumer


class UseCaseLiveNotifications(TransactionTestCase):

    def open_websocket_for_user(self, username):
        communicator =  WebsocketCommunicator(NotificationsConsumer.as_asgi(), 'ws://'
            + '127.0.0.1:8000'
            + '/ws/notification/'
            + username
            + '/')
        communicator.scope["user"] = username
        return communicator

    def setUp(self) -> None:
        # --------------- SetUp ---------------------------------
        self.market_proxy = MarketProxyBridge(MarketRealBridge())
        self.user_proxy = UserProxyBridge(UserRealBridge())
        self.user_proxy.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(self.admin_id, "manager", "1234")

        # create 4 users
        self.__guestId = self.user_proxy.login_guest().getData().getUserID()
        self.__guestId2 = self.user_proxy.login_guest().getData().getUserID()
        self.__guestId3 = self.user_proxy.login_guest().getData().getUserID()
        self.__guestId4 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        self.user_proxy.register("user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        self.user_proxy.register("user3", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        self.user_proxy.register("user4", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)

        # login 4 users
        self.user = self.user_proxy.login_member(self.__guestId, "user1", "1234").getData()
        self.user2 = self.user_proxy.login_member(self.__guestId2, "user2", "1234").getData()
        self.user3 = self.user_proxy.login_member(self.__guestId3, "user3", "1234").getData()
        self.user4 = self.user_proxy.login_member(self.__guestId4, "user4", "1234").getData()

        self.user_id = self.user.getUserID()
        self.user_id2 = self.user2.getUserID()
        self.user_id3 = self.user3.getUserID()
        self.user_id4 = self.user4.getUserID()

        # create 3 stores
        self.store_0 = self.user_proxy.open_store("s0", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, 0).getData().getStoreId()
        self.store_1 = self.user_proxy.open_store("s1", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, 0).getData().getStoreId()
        self.store_2 = self.user_proxy.open_store("s2", self.user_id4, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, 0).getData().getStoreId()

        # add products to stores
        self.product01 = self.market_proxy.add_product_to_store(self.store_0, self.user_id, "Product-01", 100,
                                                                "Category", 8,
                                                                ["Test1", "Test2"]).getData().getProductId()
        self.product02 = self.market_proxy.add_product_to_store(self.store_0, self.user_id, "Product-02", 150,
                                                                "Category", 9,
                                                                ["Test1", "Test2"]).getData().getProductId()
        self.product1 = self.market_proxy.add_product_to_store(self.store_1, self.user_id, "Product-1", 100,
                                                               "Category", 10,
                                                               ["Test1", "Test2"]).getData().getProductId()
        self.product2 = self.market_proxy.add_product_to_store(self.store_2, self.user_id4, "Product-2", 10,
                                                               "Category", 11,
                                                               ["Test1", "Test2"]).getData().getProductId()

        self.market_proxy.add_quantity_to_store(self.store_0, self.user_id, self.product01, 100)
        self.market_proxy.add_quantity_to_store(self.store_0, self.user_id, self.product02, 100)
        self.market_proxy.add_quantity_to_store(self.store_1, self.user_id, self.product1, 100)
        self.market_proxy.add_quantity_to_store(self.store_2, self.user_id4, self.product2, 100)

    def tearDown(self) -> None:
        self.market_proxy.removeStoreForGood(self.user_id, self.store_0)
        self.market_proxy.removeStoreForGood(self.user_id, self.store_1)
        self.market_proxy.removeStoreForGood(self.user_id4, self.store_2)
        # remove users
        self.user_proxy.removeMember("manager", "user1")
        self.user_proxy.removeMember("manager", "user2")
        self.user_proxy.removeMember("manager", "user3")
        self.user_proxy.removeMember("manager", "user4")
        self.user_proxy.removeSystemManger_forTests("manager")

    @pytest.mark.asyncio
    async def test_one_costumer_purchase(self):
        # --------------- Open WebSocket and Send Notification ---------------------------------
        communicator = self.open_websocket_for_user(self.user.getMemberName())
        connected, subprotocol = await communicator.connect()
        assert connected
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_1, self.product1, 10)
        self.user_proxy.purchase_product(self.user_id2, "1234123412341234", "2", "27", "Rotem", "123", "123")

        # --------------- Receive notification and close websocket ---------------------------------
        response = await communicator.receive_from()
        response = response[1:-1]
        expected = 'user ' + str(self.user_id2) + ' bought from store ' + str(self.store_0)
        print(response)
        assert response == expected
        await communicator.disconnect()

    @pytest.mark.asyncio
    async def test_several_owners_purchase(self):
        self.market_proxy.appoint_store_owner(self.store_0, self.user_id, self.user4.getMemberName())
        # --------------- Open WebSocket and Send Notification ---------------------------------
        user1_websocket = self.open_websocket_for_user(self.user.getMemberName())
        user4_websocket = self.open_websocket_for_user(self.user4.getMemberName())
        connected1, subprotocol1 = await user1_websocket.connect()
        connected4, subprotocol4 = await user4_websocket.connect()
        assert connected1 and connected4
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_1, self.product1, 10)
        self.user_proxy.purchase_product(self.user_id2, "1234123412341234", "2", "27", "Rotem", "123", "123")

        # --------------- Receive notification and close websocket ---------------------------------
        response1 = await user1_websocket.receive_from()
        response1 = response1[1:-1]
        expected = 'user ' + str(self.user_id2) + ' bought from store ' + str(self.store_0)
        assert response1 == expected
        await user1_websocket.disconnect()

        response4 = await user4_websocket.receive_from()
        response4 = response4[1:-1]
        assert response4 == expected
        await user4_websocket.disconnect()




if __name__ == '__main__':
    pytest.main()
