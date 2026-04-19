from flask import Flask, request, jsonify, render_template
from parking_system import lot, VEHICLE_TYPES

app = Flask(__name__)


# ── Главная страница ──
@app.route("/")
def index():
    return render_template("index.html")


# ── API: Статус парковки ──
@app.route("/api/status")
def api_status():
    return jsonify(lot.get_status())


# ── API: Зарегистрировать автомобиль ──
@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json()
    plate = data.get("plate", "").strip()
    owner = data.get("owner", "").strip()
    vtype = data.get("type", "car").lower()

    if not plate or not owner:
        return jsonify({"error": "Номер и владелец обязательны"}), 400
    if vtype not in VEHICLE_TYPES:
        return jsonify({"error": "Тип: car, truck, motorcycle"}), 400

    try:
        vehicle = VEHICLE_TYPES[vtype](plate, owner)
        lot.register_vehicle(vehicle)
        return jsonify({"success": True, "message": f"{plate} зарегистрирован", "vehicle": vehicle.to_dict()})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ── API: Въезд ──
@app.route("/api/enter", methods=["POST"])
def api_enter():
    data = request.get_json()
    plate = data.get("plate", "").strip()
    if not plate:
        return jsonify({"error": "Укажите номер"}), 400
    try:
        spot_id = lot.enter(plate)
        return jsonify({"success": True, "message": f"{plate.upper()} → место #{spot_id}", "spot_id": spot_id})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ── API: Выезд ──
@app.route("/api/exit", methods=["POST"])
def api_exit():
    data = request.get_json()
    plate = data.get("plate", "").strip()
    if not plate:
        return jsonify({"error": "Укажите номер"}), 400
    try:
        record = lot.exit_vehicle(plate)
        return jsonify({"success": True, "record": record.to_dict()})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ── API: Поиск ──
@app.route("/api/search")
def api_search():
    plate = request.args.get("plate", "").strip()
    if not plate:
        return jsonify({"error": "Укажите номер"}), 400
    result = lot.search(plate)
    return jsonify(result)


# ── API: История ──
@app.route("/api/history")
def api_history():
    return jsonify(lot.get_history())


# ── API: Реестр ──
@app.route("/api/registry")
def api_registry():
    return jsonify(lot.get_registry())


if __name__ == "__main__":
    app.run(debug=True)
