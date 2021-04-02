from aiohttp import web
from admin.views import *


def setup_admin_routes(app: web.Application):
    app.router.add_get("/admin", admin_index, name="admin_index")
    app.router.add_get("/admin/users", admin_users, name='admin_users')
    app.router.add_get("/admin/products", admin_products, name="admin_products")
    app.router.add_get("/admin/users/details/{id}", admin_user_details, name="admin_user_details")
    app.router.add_get("/admin/products/details/{id}", admin_product_details, name="admin_product_details")
    app.router.add_get("/admin/users/details/{id}/edit", admin_user_edit, name="admin_user_edit")
    app.router.add_post("/admin/users/details/{id}/edit", admin_user_edit_post)
    app.router.add_get("/admin/products/{id}/edit", admin_product_edit, name="admin_product_edit")
    app.router.add_post("/admin/products/{id}/edit", admin_product_edit_post)
    app.router.add_get("/admin/products/create", admin_product_create, name="admin_product_create")
    app.router.add_post("/admin/products/create", admin_product_create_post)
    app.router.add_get("/admin/users/create", admin_user_create, name="admin_user_create")
    app.router.add_post("/admin/users/create", admin_user_create_post)
    app.router.add_get("/admin/users/{id}/delete", admin_user_delete, name="admin_user_delete")
    app.router.add_post("/admin/users/{id}/delete", admin_user_delete_post)
    app.router.add_get("/admin/products/{id}/delete", admin_product_delete, name="admin_product_delete")
    app.router.add_post("/admin/products/{id}/delete", admin_product_delete_post)
