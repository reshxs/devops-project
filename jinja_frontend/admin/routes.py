from jinja_frontend.admin.views import *


def setup_admin_routes(app):
    app.router.add_get("/admin", admin_index, name="admin_index")
    app.router.add_get("/admin/users", admin_users, name='admin_users')
    app.router.add_get("/admin/products", admin_products, name="admin_products")
    app.router.add_get("/admin/users/{id}", admin_user_details, name="admin_user_details")
    app.router.add_get("/admin/products/{id}", admin_product_details, name="admin_product_details")
    app.router.add_get("/admin/users/{id}/edit", admin_user_edit, name="admin_user_edit")
    app.router.add_post("/admin/users/{id}/edit", admin_user_edit_post)
    app.router.add_get("/admin/products/{id}/edit", admin_product_edit, name="admin_product_edit")
    app.router.add_post("/admin/products/{id}/edit", admin_product_edit_post)