from flask import redirect,render_template,request,session,url_for,flash
from webblog.Forms import Registerform,LoginForm,AddPost,UpdatePost
from webblog import app,db,bcrypt
from webblog.Models import User,Post

import os
import secrets

from flask_login import login_user,current_user,logout_user,login_required





@app.route('/',methods=['GET','POST'])
def Index():

    post=Post.query.order_by('date').all()
    
    return render_template('index.html',posts=reversed(post))
    



@app.route('/register',methods=['GET','POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('Index'))
    form=Registerform()
    if request.method=='POST':
        if form.validate_on_submit():
            encrypt_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user=User(username=form.username.data,email=form.email.data,password=encrypt_password)
            db.session.add(user)
            db.session.commit()
            
            flash('Register Successful','success')
            return redirect(url_for('Login'))
        else:
            flash('Invalid Inputs','danger')
    return render_template('register_form.html' ,form=form)



@app.route('/login',methods=['GET','POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Index'))
    form=LoginForm()

    if request.method=='POST':
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)
                return redirect(url_for('Index'))
            else:
                
                flash('Login Unsuccessful. Please check email and password!','danger')
                return redirect(url_for('Login'))


    return render_template('login.html',form=form)


@app.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('Index'))



@app.route('/add',methods=['GET','POST'])
@login_required
def Add():
    if not current_user.is_authenticated:
        flash('You can not add a post!')
        return redirect(url_for('Index'))

    add_form=AddPost()    

    
    if request.method=='POST':
        image_path_for_database=save_image(add_form.image.data).split('webblog')[-1]
        image_path=f'..{image_path_for_database}'

        post=Post(content=add_form.content.data,image=image_path,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()

        print(add_form.image.data)

        return redirect(url_for('Index'))
            

        
            
    

    return render_template('add.html',form=add_form)

def save_image(image_file):
    _,ext=os.path.splitext(image_file.filename)

    image_name=secrets.token_hex(10)+ext
    image_path=os.path.join(app.root_path,'static','images','posts',image_name)
    
    image_file.save(image_path)

    

    return image_path



@app.route('/post_update/<int:post_id>',methods=['GET','POST'])
@login_required
def EditPost(post_id):

    form=UpdatePost()
    
    
    post=Post.query.get_or_404(int(post_id))
    form.content.data=post.content
    

    if request.method=='POST':
        new_image=form.image.data
        new_content=form.content.data

        post.content=new_content
        # print(form.image.data.filename)
        image_path_for_database=save_image(form.image.data).split('webblog')[-1]
        post.image=f'..{image_path_for_database}'

        db.session.commit()
        
        
        
        return redirect(url_for('Index'))

    return render_template('update.html',post=post,form=form)


@app.route('/delete/<int:id>')
@login_required

def Delete(id):

    post=Post.query.get_or_404(int(id))
    db.session.delete(post)
    db.session.commit()
    
    
    return redirect(url_for('Index'))




@app.route(f'/user')
def UserAccount():

    

    return f'<p>{current_user.username}</p>'


@app.route('/account/<string:name>_<int:id>')
def Account(name,id):
    if current_user.is_authenticated:
        if name==current_user.username:
            return redirect(url_for("UserAccount"))
        else:
            post=Post.query.filter_by(user_id=id)
            return render_template('index.html',posts=post)

    else:
        flash('You first need to login','warning')
        return redirect(url_for("Login"))        
    
    

    
