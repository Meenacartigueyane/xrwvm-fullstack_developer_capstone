from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    car_make_instances = []

    for data in car_make_data:
        car_make_instances.append(
            CarMake.objects.create(
                name=data["name"],
                description=data["description"]
            )
        )

    car_model_data = [
        ("Pathfinder", "SUV", car_make_instances[0]),
        ("Qashqai", "SUV", car_make_instances[0]),
        ("XTRAIL", "SUV", car_make_instances[0]),
        ("A-Class", "SUV", car_make_instances[1]),
        ("C-Class", "SUV", car_make_instances[1]),
        ("E-Class", "SUV", car_make_instances[1]),
        ("A4", "SUV", car_make_instances[2]),
        ("A5", "SUV", car_make_instances[2]),
        ("A6", "SUV", car_make_instances[2]),
        ("Sorrento", "SUV", car_make_instances[3]),
        ("Carnival", "SUV", car_make_instances[3]),
        ("Cerato", "SEDAN", car_make_instances[3]),
        ("Corolla", "SEDAN", car_make_instances[4]),
        ("Camry", "SEDAN", car_make_instances[4]),
        ("Kluger", "SUV", car_make_instances[4]),
    ]

    for name, car_type, make in car_model_data:
        CarModel.objects.create(
            name=name,
            car_make=make,
            type=car_type,
            year=2023,
            dealer_id=0
        )git add server/djangoapp/populate.py