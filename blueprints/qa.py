from flask import Blueprint, render_template, g, request, redirect, url_for, flash
from decorators import login_required
from .forms import QuestionForm
from models import QuestionModel
from exts import db

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    # questions = QuestionModel.query.order_by(db.text("-create_time")).all()
    # return render_template("Refrigerator/meidibig.html", questions=questions)
    return render_template("index.html")


@bp.route("/xiangqing/<int:commodity_id>")
def commodity_detail(commodity_id):
    # question = QuestionModel.query.get(commodity_id)
    questions = QuestionModel.query.order_by(db.text("-create_time")).filter_by(commodity_id=commodity_id)
    if commodity_id == 1:
        return render_template("Refrigerator/meidibig.html", questions=questions)
    elif commodity_id == 2:
        return render_template("Refrigerator/meidismall.html", questions=questions)
    elif commodity_id == 3:
        return render_template("Refrigerator/haierbig.html", questions=questions)
    elif commodity_id == 4:
        return render_template("Refrigerator/haiersmall.html", questions=questions)
    elif commodity_id == 5:
        return render_template("Refrigerator/rongshengbig.html", questions=questions)
    elif commodity_id == 6:
        return render_template("Refrigerator/rongshengsmall.html", questions=questions)
    elif commodity_id == 7:
        return render_template("milk powder/atm.html", questions=questions)
    elif commodity_id == 8:
        return render_template("milk powder/meisu.html", questions=questions)
    elif commodity_id == 9:
        return render_template("milk powder/meizc.html", questions=questions)
    elif commodity_id == 10:
        return render_template("milk powder/huis.html", questions=questions)
    elif commodity_id == 11:
        return render_template("milk powder/feihe.html", questions=questions)
    elif commodity_id == 12:
        return render_template("milk powder/quec.html", questions=questions)
    elif commodity_id == 13:
        return render_template("lxz/dangni.html", questions=questions)
    elif commodity_id == 14:
        return render_template("lxz/jinfang.html", questions=questions)
    elif commodity_id == 15:
        return render_template("lxz/piaowdm.html", questions=questions)
    elif commodity_id == 16:
        return render_template("test1111.html", questions=questions)


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template("detail.html", question=question)


@bp.route("/question/public/<int:name>", methods=['GET', 'POST'])
@login_required
def public_question(name):
    print(name)
    # 判断是否登录，如果没有跳转到登录页面
    if request.method == 'GET':
        return render_template("public_question.html",name=name)
    else:
        form = QuestionForm(request.form)
        if form.validate():
            content = form.content.data
            question = QuestionModel(content=content, author=g.user,commodity_id=name)
            # question = QuestionModel( content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # return redirect("/")
            return redirect(url_for("qa.commodity_detail", commodity_id=name))

        else:
            flash("标题或内容格式错误！！")
            return redirect(url_for("qa.public_question"))



