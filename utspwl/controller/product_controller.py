import json
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.request import Request

from sqlalchemy.exc import DBAPIError


from ..models import Product


@view_defaults(route_name="product")
class ProductView:
    def __init__(self, request):
        self.request: Request = request

    @view_config(request_method="POST", permission="admin")
    def create(self):
        try:
            try:
                name = self.request.json_body["name"]
                price = self.request.json_body["price"]
                gambar = self.request.json_body["gambar"]
                stok = self.request.json_body["stok"]
            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps({"error": "title or content is empty"}),
                )

            produk = Product(name = name, price = price, gambar = gambar, stok = stok)
            self.request.dbsession.add(produk)
            self.request.dbsession.flush()
            
            product_data = {
            "name": produk.name,
            "price": produk.price,
            "gambar": produk.gambar,
            "stok": produk.stok
        }

            return Response(
                json={"message": "success", "data" : product_data},
                status=200,
                content_type="application/json",
            )

        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )

    @view_config(request_method="GET", permission="view")
    def read(self):
        try:
            produk = self.request.dbsession.query(Product).all()
            return Response(
                json={
                    "data": [
                        {
                            "id": produks.id,
                            "name": produks.name,
                            "price": produks.price,
                            "stok" : produks.stok
                        }
                        for produks in produk
                    ]
                },
                status=200,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json=json.dumps({"message": "failed"}),
                status=500,
                content_type="application/json",
            )

    @view_config(request_method="PUT", permission="admin")
    def update(self):
        try:
            try:
                id = self.request.json_body["id"]
                name = self.request.json_body["name"]
                price = self.request.json_body["price"]
                gambar = self.request.json_body["gambar"]
                stok = self.request.json_body["stok"]
            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps({"error": "id, title or content is empty"}),
                )

            produk = self.request.dbsession.query(Product).filter_by(id=id).first()

            produk.name = name
            produk.price = price
            produk.gambar = gambar
            produk.stok = stok

            self.request.dbsession.flush()

            return Response(
                json={"message": "success"},
                status=201,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )

    @view_config(request_method="DELETE", permission="admin")
    def delete(self):
        try:
            try:
                id = self.request.json_body["id"]
            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps({"error": "id is empty"}),
                )

            produk = self.request.dbsession.query(Product).filter_by(id=id).first()
            self.request.dbsession.delete(produk)
            self.request.dbsession.flush()

            return Response(
                json={"message": "success"},
                status=200,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )
