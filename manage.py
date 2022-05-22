#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from threading import Thread

from Backend.Service.Initializer import Initializer

sys.path.append('....')
from Backend.Service.DTO.GuestDTO import GuestDTO
from Backend.Service.DTO.MemberDTO import MemberDTO
from Backend.Service.DTO.ProductDTO import ProductDTO
from Backend.Service.DTO.StoreDTO import StoreDTO


def web_run():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frontend.settings')
    initialize_system()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def initialize_system():
    initializer = Initializer()
    role_service = initializer.getRoleService()
    member_service = initializer.getMemberService()
    user_service = initializer.getUserService()
    guest: GuestDTO = user_service.enterSystem().getData()
    user_service.memberSignUp("ori", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 1)
    user_service.memberSignUp("rotem", "1234", "0540000000", 123, 2, "Israel", "Beer Sheva", "Rager", 1, 1)
    user_service.memberSignUp("bar", "1234", "0540000000", 123, 3, "Israel", "Beer Sheva", "Rager", 1, 1)
    user_service.memberSignUp("kfir", "1234", "0540000000", 123, 3, "Israel", "Beer Sheva", "Rager", 1, 1)
    user_service.memberSignUp("niv", "1234", "0540000000", 123, 3, "Israel", "Beer Sheva", "Rager", 1, 1)
    user1: MemberDTO = user_service.memberLogin(guest.getUserID(), "ori", "1234").getData()
    user1Id = user1.getUserID()
    user1name = user1.getMemberName()
    store1: StoreDTO = member_service.createStore("o1", user1.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    store2: StoreDTO = member_service.createStore("o2", user1.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    computer: ProductDTO = role_service.addProductToStore(store1.getStoreId(), user1.getUserID(), "Computer", 3000,
                                                          "Electric Devices", 50,
                                                          ["Electric Device", "Computer", "Check"]).getData()
    role_service.addProductQuantityToStore(store1.getStoreId(), user1.getUserID(), computer.getProductId(), 1000)
    camera: ProductDTO = role_service.addProductToStore(store1.getStoreId(), user1.getUserID(), "Camera", 1000,
                                                        "Electric Devices", 20, []).getData()
    role_service.addProductQuantityToStore(store1.getStoreId(), user1.getUserID(), camera.getProductId(), 500)
    cases: ProductDTO = role_service.addProductToStore(store1.getStoreId(), user1.getUserID(), "Phone Case", 50,
                                                       "Phone Accessories", 5, []).getData()
    role_service.addProductQuantityToStore(store1.getStoreId(), user1.getUserID(), cases.getProductId(), 3000)
    role_service.addProductToStore(store2.getStoreId(), user1.getUserID(), "Bed Sheets", 200, "Sheets", 8, [])
    role_service.addProductToStore(store2.getStoreId(), user1.getUserID(), "Pillow", 100, "Pillows", 5, [])
    member_service.logoutMember("ori")
    guest = user_service.enterSystem().getData()
    user: MemberDTO = user_service.memberLogin(guest.getUserID(), "bar", "1234").getData()
    store3: StoreDTO = member_service.createStore("b1", user.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    cola: ProductDTO = role_service.addProductToStore(store3.getStoreId(), user.getUserID(), "Cola", 15,
                                                      "Drinks", 8, []).getData()
    role_service.addProductQuantityToStore(store3.getStoreId(), user.getUserID(), cola.getProductId(), 2000)
    orange_juice: ProductDTO = role_service.addProductToStore(store3.getStoreId(), user.getUserID(), "Orange Juice", 11,
                                                              "Drinks", 8, []).getData()
    role_service.addProductQuantityToStore(store3.getStoreId(), user.getUserID(), orange_juice.getProductId(), 3000)
    store4: StoreDTO = member_service.createStore("b2", user.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    member_service.logoutMember("bar")
    guest: GuestDTO = user_service.enterSystem().getData()
    user: MemberDTO = user_service.memberLogin(guest.getUserID(), "rotem", "1234").getData()
    store5: StoreDTO = member_service.createStore("r1", user.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    store6: StoreDTO = member_service.createStore("r2", user.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    product1: ProductDTO = role_service.addProductToStore(store5.getStoreId(), user.getUserID(), "Shirt", 100,
                                                          "Clothing", 2, []).getData()
    role_service.addProductQuantityToStore(store5.getStoreId(), user.getUserID(), product1.getProductId(), 50)
    product2: ProductDTO = role_service.addProductToStore(store5.getStoreId(), user.getUserID(), "Pants", 200,
                                                          "Clothing", 2, []).getData()
    role_service.addProductQuantityToStore(store5.getStoreId(), user.getUserID(), product2.getProductId(), 100)
    role_service.appointManagerToStore(store5.getStoreId(), user.getUserID(), user1name)
    role_service.setRolesInformationPermission(store5.getStoreId(), user.getUserID(), user1name)
    role_service.setStockManagerPermission(store5.getStoreId(), user.getUserID(), user1name)
    member_service.logoutMember("rotem")
    kfir: MemberDTO = user_service.memberLogin(guest.getUserID(), "kfir", "1234").getData()
    user_service.addProductToCart(kfir.getUserID(), 0, 0, 2)
    user_service.purchaseCart(kfir.getUserID(), 1, 1)
    member_service.logoutMember("kfir")
    niv: MemberDTO = user_service.memberLogin(guest.getUserID(), "niv", "1234").getData()
    user_service.addProductToCart(niv.getUserID(), 0, 0, 1)
    user_service.addProductToCart(niv.getUserID(), store3.getStoreId(), cola.getProductId(), 10)
    user_service.purchaseCart(niv.getUserID(), 1, 1)
    member_service.logoutMember("niv")


def main():
    web_run()


if __name__ == '__main__':
    main()
