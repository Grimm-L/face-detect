from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        "menus": [
            {
                "orderId": "20220224150653149",
                "orderCategory": 3,
                "username": "刘子添",
                "userId": 6,
                "phone": "13676087366",
                "price": 17.50,
                "money": 1598.50,
                "num": 2,
                "status": "已支付",
                "orderTime": "2022-02-24T07:06:54.000+00:00",
                "determineTime": 1,
                "orderDetails": [
                    {
                        "id": 128,
                        "orderId": "20220224150653149",
                        "vegetableId": 177,
                        "vegetableName": "白切鸡",
                        "vegetablePrice": 10.00,
                        "vegetableNum": 1,
                        "vegetableImage": "http://47.112.29.9/images/default.jpg"
                    },
                    {
                        "id": 129,
                        "orderId": "20220224150653149",
                        "vegetableId": 178,
                        "vegetableName": "香菇焖鸡",
                        "vegetablePrice": 7.50,
                        "vegetableNum": 1,
                        "vegetableImage": "http://47.112.29.9/images/default.jpg"
                    }
                ]
            },
            {
                "orderId": "20220224150653150",
                "orderCategory": 3,
                "username": "刘子添",
                "userId": 6,
                "phone": "13676087366",
                "price": 17.50,
                "money": 1598.50,
                "num": 2,
                "status": "已支付",
                "orderTime": "2022-02-24T07:06:54.000+00:00",
                "determineTime": 1,
                "orderDetails": [
                    {
                        "id": 128,
                        "orderId": "20220224150653149",
                        "vegetableId": 177,
                        "vegetableName": "鸡蛋瘦肉粥",
                        "vegetablePrice": 10.00,
                        "vegetableNum": 1,
                        "vegetableImage": "http://47.112.29.9/images/default.jpg"
                    },
                    {
                        "id": 129,
                        "orderId": "20220224150653149",
                        "vegetableId": 178,
                        "vegetableName": "大葱炒大蒜",
                        "vegetablePrice": 7.50,
                        "vegetableNum": 1,
                        "vegetableImage": "http://47.112.29.9/images/default.jpg"
                    }
                ]
            },
            {
                "orderId": "20220224150653150",
                "orderCategory": 3,
                "username": "刘子添",
                "userId": 6,
                "phone": "13676087366",
                "price": 17.50,
                "money": 1598.50,
                "num": 2,
                "status": "已支付",
                "orderTime": "2022-02-24T07:06:54.000+00:00",
                "determineTime": 1,
                "orderDetails": [
                    {
                        "id": 128,
                        "orderId": "20220224150653149",
                        "vegetableId": 177,
                        "vegetableName": "鸡蛋瘦肉粥",
                        "vegetablePrice": 10.00,
                        "vegetableNum": 1,
                        "vegetableImage": "http://47.112.29.9/images/default.jpg"
                    },
                    {
                        "id": 129,
                        "orderId": "20220224150653149",
                        "vegetableId": 178,
                        "vegetableName": "大葱炒大蒜",
                        "vegetablePrice": 7.50,
                        "vegetableNum": 1,
                        "vegetableImage": "http://47.112.29.9/images/default.jpg"
                    }
                ]
            }
        ]
    }
    return render(request, 'faceui/index.html', context)
