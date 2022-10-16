
from app import current_app, db
from app.model import Admin, UserLogins, Blog, Join_Requests
from flask import request, jsonify

from app.web_app import web_app_blueprint as blp
from flask_jwt_extended import jwt_required, create_access_token, get_current_user

@blp.route('/auth/token', methods=["POST"])
def auth_token():
    user_id = request.form.get("user_id")
    password = request.form.get("password")

    if user_id is None:
        return jsonify({"error": "Missing user id"}), 400
    if password is None:
        return jsonify({"error": "Missing password"}), 400

    check, user = Admin.is_admin_user(user_id, password)
    if check:
        token = create_access_token(user_id, password)
        # user_login_states = UserLogins(user)
        # db.session.add(user_login_states)
        db.session.commit()
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"error": "Incorrect user id"}), 400


@blp.route("/post_new_block", methods=["POST"])
@jwt_required()
def post_new_block():
    heading = request.form.get("heading")
    image_link = request.form.get("image_link")
    body = request.form.get("body")
    admin = get_current_user()
    if heading is None:
        return jsonify({"error": "Missing heading."}), 400
    if body is None:
        return jsonify({"error": "Missing blog body."}), 400
    blog_obj = Blog(heading, body, image_link, admin.admin_id) # making blog object
    db.session.add(blog_obj)
    db.session.commit()
    return jsonify(msg="Blog posted successfully"), 200


# non-jwt protected endpoint
@blp.route("/view_blogs", methods=["GET"])
def view_blogs():
    # taking per_page count
    per_page = request.args.get("per_page", "20")
    if per_page.strip().isnumeric():
        per_page = int(per_page)
    else:
        per_page = 20
    # taking page count
    page = request.args.get("page", "1")
    if page.strip().isnumeric():
        page = int(page)
    else:
        page = 1
    blogs = Blog.query.paginate(per_page = per_page, page = page)
    response = [blog.to_dict() for blog in blogs.items] # getting the blog data in dict

    return jsonify(response = response), 200


# non-jwt protected endpoint
@blp.route("/view_blog_by_id", methods=["GET"])
def view_blog_by_id():
    # taking the blog id
    blog_id = request.args.get("blog_id", None)
    if blog_id.strip().isnumeric():
        blog_id = int(blog_id)
    else:
        return jsonify({"error": "Blog id must be a number"}), 400

    blog = Blog.query.get(blog_id)
    if blog:
        return jsonify({"response": blog.to_dict()}), 200
    else:
        return jsonify({"error": "Blog not found."}), 404


# non-jwt protected endpoint
@blp.route("/blog_by_writer", methods=["GET"])
def blog_by_writter():
    # taking writer user_id
    user_id = request.args.get('user_id')

    # taking per_page count
    per_page = request.args.get("per_page", "20")
    if per_page.strip().isnumeric():
        per_page = int(per_page)
    else:
        per_page = 1
    
    # taking page count
    page = request.args.get("page", "1")
    if page.strip().isnumeric():
        page = int(page)
    else:
        page = 1
    blogs = Blog.query.filter_by(admin_id=user_id).paginate(per_page=per_page, page=page)
    response = [blog.to_dict() for blog in blogs.items]

    return jsonify(response= response)


##################
# Update Product #
##################

@blp.route("/update_blog", methods=["POST"])
@jwt_required()
def update_blog():
    current_user = get_current_user()

    # get blog id
    blog_id = request.form.get("blog_id")
    blog_heading = request.form.get("blog_heading", "").strip()
    blog_body = request.form.get("blog_body", "").strip()
    blog_image_link = request.form.get("blog_image_link", "").strip()

    blog = Blog.query.get(blog_id)
    blog.update(blog_heading, blog_body, blog_image_link)
    db.session.commit()
    return jsonify(response = "Blog Updated successfully!")


#delete blog
@blp.route('/delete_blog')
@jwt_required()
def delete_blog():
    # getting the blog id
    blog_id = request.args.get('blog_id')
    blog = Blog.query.get(blog_id)
    if blog is not None:
        db.session.delete(blog)
        db.session.commit()
        return jsonify(response = "Blog Deleted successfully!"), 200
    else:
        return jsonify(response = "No such blog!"), 404



# non jwt protected endpoints
@blp.route("/join_ecell", methods=["POST"])
def join_ecell():
    name = request.form.get("name")
    email = request.form.get("email")
    number = request.form.get("number")
    roll = request.form.get("roll")

    if name is not None and email is not None and number is not None and roll is not None:
        join_req = Join_Requests(name, email, number, roll)
        db.session.add(join_req)
        db.session.commit()
        return jsonify(response = "Ecell Join Successfully!"), 200
    else:
        return jsonify(response = "Please send all fields to join"), 200


@blp.route("/get_join_requests")
@jwt_required()
def get_join_requests():
    response = [join_req.to_dict for join_req in Join_Requests.query.filter_by(reviewed = False).all()]
    return jsonify(response = response)


@blp.route('/marks_join_request_viewed')
@jwt_required()
def mark_join_request_viewed():
    _id = request.args.get("id")
    join_req = Join_Requests.query.get(id=_id)
    if join_req is None:
        return jsonify(response = "No Join Request Found"), 404
    join_req.reviewed = True
    db.session.commit()
    return jsonify(response = "Reviewed!"), 200


@blp.route("/connect", methods=["POST"])
def connect():
    profession = request.form.get("profession")
    email = request.form.get("email")
    number = request.form.get("number")
    field = request.form.get("field")

    if profession is not None and email is not None and number is not None and field is not None:
        contacts = Contacts(profession, email, number, field)
        db.session.add(contacts)
        db.session.commit()
        return jsonify(response = "Success!"), 200
    else:
        return jsonify(response = "Incorrect Request"), 400

@blp.route("/get_contacts")
@jwt_required()
def get_contacts():
    response = [contact.to_dict for contact in Contacts.query.all()]
    return jsonify(response = response), 200