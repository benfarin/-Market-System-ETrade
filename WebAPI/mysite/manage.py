#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from threading import Thread

from Service.DTO.MemberDTO import MemberDTO
from Service.DTO.ProductDTO import ProductDTO
from Service.DTO.StoreDTO import StoreDTO
from Service.MemberService import MemberService
from Service.RoleService import RoleService
from Service.UserService import UserService

sys.path.append('....')


def web_run():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
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
    role_service = RoleService()
    member_service = MemberService()
    user_service = UserService()

    user_service.memberSignUp("ori", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 1)
    user_service.memberSignUp("rotem", "1234", "0540000000", 123, 2, "Israel", "Beer Sheva", "Rager", 1, 1)
    user_service.memberSignUp("bar", "1234", "0540000000", 123, 3, "Israel", "Beer Sheva", "Rager", 1, 1)
    user1: MemberDTO = user_service.memberLogin("ori", "1234").getData()
    user1Id = user1.getUserID()
    store1: StoreDTO = member_service.createStore("o1", user1.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    store2: StoreDTO = member_service.createStore("o2", user1.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    computer: ProductDTO = role_service.addProductToStore(store1.getStoreId(), user1.getUserID(), "Computer", 3000,
                                                          "Electric Devices", []).getData()
    role_service.addProductQuantityToStore(store1.getStoreId(), user1.getUserID(), computer.getProductId(), 1000)
    camera: ProductDTO = role_service.addProductToStore(store1.getStoreId(), user1.getUserID(), "Camera", 1000,
                                                        "Electric Devices", []).getData()
    role_service.addProductQuantityToStore(store1.getStoreId(), user1.getUserID(), camera.getProductId(), 500)
    cases: ProductDTO = role_service.addProductToStore(store1.getStoreId(), user1.getUserID(), "Phone Case", 50,
                                                       "Phone Accessories", []).getData()
    role_service.addProductQuantityToStore(store1.getStoreId(), user1.getUserID(), cases.getProductId(), 3000)
    role_service.addProductToStore(store2.getStoreId(), user1.getUserID(), "Bed Sheets", 200, "Sheets", [])
    role_service.addProductToStore(store2.getStoreId(), user1.getUserID(), "Pillow", 100, "Pillows", [])
    member_service.logoutMember("ori")
    user: MemberDTO = user_service.memberLogin("bar", "1234").getData()
    store3: StoreDTO = member_service.createStore("b1", user.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    store4: StoreDTO = member_service.createStore("b2", user.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    member_service.logoutMember("bar")
    user: MemberDTO = user_service.memberLogin("rotem", "1234").getData()
    store5: StoreDTO = member_service.createStore("r1", user.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    store6: StoreDTO = member_service.createStore("r2", user.getUserID(), 1, 1, "Israel", "Beer Sheva", "Kadesh", 1,
                                                  1).getData()
    product1: ProductDTO = role_service.addProductToStore(store5.getStoreId(), user.getUserID(), "Shirt", 100,
                                                          "Clothing", []).getData()
    role_service.addProductQuantityToStore(store5.getStoreId(), user.getUserID(), product1.getProductId(), 50)
    product2: ProductDTO = role_service.addProductToStore(store5.getStoreId(), user.getUserID(), "Pants", 200,
                                                          "Clothing", []).getData()
    role_service.addProductQuantityToStore(store5.getStoreId(), user.getUserID(), product2.getProductId(), 100)
    role_service.appointManagerToStore(store5.getStoreId(), user.getUserID(), user1Id)
    role_service.setRolesInformationPermission(store5.getStoreId(), user.getUserID(), user1Id)
    member_service.logoutMember("rotem")


def main():
    initialize_system()
    t = Thread(target=web_run, args=(), )
    t.run()


if __name__ == '__main__':
    main()
