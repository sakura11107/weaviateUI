from flask import Blueprint, request, jsonify
from weaviate_client import *

bp = Blueprint('api', __name__, url_prefix='/api')

# 列出所有类（schema）
@bp.route('/classes', methods=['GET'])
def list_classes():
    res = weaviate_get('/schema')
    return jsonify(res.json()), res.status_code

# 新增类
@bp.route('/classes', methods=['POST'])
def create_class():
    res = weaviate_post('/schema', request.json)
    return jsonify(res.json()), res.status_code

# 删除类
@bp.route('/classes/<class_name>', methods=['DELETE'])
def delete_class(class_name):
    res = weaviate_delete(f'/schema/{class_name}')
    return jsonify(res.json() if res.content else {}), res.status_code

# 新增对象
@bp.route('/objects', methods=['POST'])
def create_object():
    res = weaviate_post('/objects', request.json)
    return jsonify(res.json()), res.status_code

# 获取对象（可选条件）
@bp.route('/objects', methods=['GET'])
def list_objects():
    res = weaviate_get('/objects')
    return jsonify(res.json()), res.status_code

# 删除对象
@bp.route('/objects/<uuid>', methods=['DELETE'])
def delete_object(uuid):
    res = weaviate_delete(f'/objects/{uuid}')
    return jsonify(res.json() if res.content else {}), res.status_code

# 获取某类下的对象列表
# 获取某类下的对象列表（带分页和总数）
@bp.route('/objects/<class_name>', methods=['GET'])
def list_objects_by_class(class_name):
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    query_string = f"/objects?class={class_name}&limit={limit}&offset={offset}"
    res = weaviate_get(query_string)
    data = res.json()

    # 使用 POST 调用 GraphQL 查询总数
    graphql_query = {
        "query": f"""
        {{
          Aggregate {{
            {class_name} {{
              meta {{
                count
              }}
            }}
          }}
        }}
        """
    }
    count_res = weaviate_post("/graphql", graphql_query)
    total = 0
    if count_res.ok:
        count_data = count_res.json()
        total = (
            count_data.get("data", {})
            .get("Aggregate", {})
            .get(class_name, [{}])[0]
            .get("meta", {})
            .get("count", 0)
        )

    return jsonify({
        "objects": data.get("objects", []),
        "total": total
    }), res.status_code


# 获取指定类的 Schema 信息
@bp.route('/classes/<class_name>/schema', methods=['GET'])
def get_class_schema(class_name):
    res = weaviate_get(f'/schema/{class_name}')
    return jsonify(res.json() if res.content else {}), res.status_code
