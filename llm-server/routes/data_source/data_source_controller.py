from models.repository.datasource_repo import (
    get_all_pdf_datasource_by_bot_id,
    get_all_website_datasource_by_bot_id,
)
from flask import Blueprint, request, jsonify
from utils.db import Database
from flask import Flask, request, jsonify, Blueprint, request, Response
from operator import itemgetter

db_instance = Database()
mongo = db_instance.get_db()

datasource_workflow = Blueprint("datasource", __name__)


@datasource_workflow.route("/b/<bot_id>", methods=["GET"])
def get_data_sources(bot_id: str) -> Response:
    limit = request.args.get("limit", 20)
    offset = request.args.get("offset", 0)

    pdf_datasources = get_all_pdf_datasource_by_bot_id(bot_id, limit, offset)

    pdf_sources = [
        {
            "id": ds.id,
            "chatbot_id": ds.created_at,
            "source": ds.file_name,
            "status": ds.status,
            "updated_at": ds.updated_at,
        }
        for ds in pdf_datasources
    ]
    web_datasources = get_all_website_datasource_by_bot_id(bot_id, limit, offset)

    web_sources = [
        {
            "id": wds.id,
            "chatbot_id": wds.created_at,
            "source": wds.url,
            "status": wds.status,
            "updated_at": wds.updated_at,
        }
        for wds in web_datasources
    ]
    return jsonify({"pdf_sources": pdf_sources, "web_sources": web_sources})
