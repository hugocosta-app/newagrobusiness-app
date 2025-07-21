from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory, abort
from app import db
from app.models.visit import Visit, VisitPhoto
from app.models.user import User # For filtering/displaying seller info
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime

bp = Blueprint("visits", __name__, url_prefix="/visits")

# Use same allowed extensions or define specific ones for photos
ALLOWED_PHOTO_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_photo_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_PHOTO_EXTENSIONS

def query_visits(apply_filters=True):
    """Helper function to query visits based on user role and filters."""
    query = Visit.query
    
    # Role-based filtering
    if not current_user.is_admin:
        query = query.filter(Visit.seller_id == current_user.id)
    
    # Add filters later if needed (e.g., date range, customer name)
    # if apply_filters:
        # ... filter logic ...
                
    return query

@bp.route("/")
@login_required
def list_visits():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    
    query = query_visits(apply_filters=False) # No filters for now
    visits_pagination = query.order_by(Visit.visit_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template("visits/list.html", 
                           visits=visits_pagination, 
                           title="Meus Relatórios de Visita" if not current_user.is_admin else "Relatórios de Visita"
                           )

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_visit():
    if request.method == "POST":
        customer_name = request.form.get("customer_name")
        visit_date_str = request.form.get("visit_date")
        city = request.form.get("city")
        state = request.form.get("state")
        products_discussed = request.form.get("products_discussed")
        summary = request.form.get("summary")
        highlights = request.form.get("highlights")
        observations = request.form.get("observations")
        photos = request.files.getlist("photos") # Handle multiple files

        # Basic Validation
        if not all([customer_name, visit_date_str, city, state, summary]):
            flash("Cliente, Data, Cidade, Estado e Resumo da Visita são obrigatórios.", "danger")
            return render_template("visits/form.html", title="Registrar Nova Visita")

        try:
            visit_date = datetime.strptime(visit_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Formato de Data inválido.", "danger")
            return render_template("visits/form.html", title="Registrar Nova Visita")

        new_visit = Visit(
            customer_name=customer_name,
            visit_date=visit_date,
            city=city,
            state=state,
            products_discussed=products_discussed,
            summary=summary,
            highlights=highlights,
            observations=observations,
            seller_id=current_user.id
        )
        db.session.add(new_visit)
        
        # Handle photo uploads
        saved_filenames = []
        upload_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "visits") # Subfolder for visit photos
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        try:
            for photo in photos:
                if photo and allowed_photo_file(photo.filename):
                    filename = secure_filename(f"visit_{current_user.id}_{int(datetime.now().timestamp())}_{photo.filename}")
                    upload_path = os.path.join(upload_folder, filename)
                    photo.save(upload_path)
                    saved_filenames.append(filename)
                    # Create VisitPhoto record
                    visit_photo = VisitPhoto(visit=new_visit, filename=filename)
                    db.session.add(visit_photo)
                elif photo:
                    # If a file is present but not allowed
                    flash(f"Tipo de arquivo inválido para foto: {photo.filename}. Apenas {ALLOWED_PHOTO_EXTENSIONS} são permitidos.", "warning")
                    # Continue processing other valid photos

            # Commit visit and photos together
            db.session.commit()
            flash("Visita registrada com sucesso!", "success")
            return redirect(url_for("visits.list_visits"))

        except Exception as e:
            db.session.rollback()
            # Clean up any saved photos if commit fails
            for fname in saved_filenames:
                fpath = os.path.join(upload_folder, fname)
                if os.path.exists(fpath):
                    try:
                        os.remove(fpath)
                    except OSError:
                        pass # Ignore cleanup error
            flash(f"Erro ao registrar visita ou salvar fotos: {e}", "danger")

    # GET request
    return render_template("visits/form.html", title="Registrar Nova Visita")

@bp.route("/view/<int:visit_id>")
@login_required
def view_visit(visit_id):
    query = Visit.query
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)
    visit = query.get_or_404(visit_id)
    return render_template("visits/view.html", visit=visit, title=f"Detalhes da Visita #{visit.id}")

@bp.route("/photos/<filename>")
@login_required
def uploaded_visit_photo(filename):
    # Security check: Ensure the user requesting the file is the owner or an admin
    photo_record = VisitPhoto.query.filter_by(filename=filename).first()
    if not photo_record:
        return abort(404)
        
    visit_record = Visit.query.get(photo_record.visit_id)
    if not visit_record:
         return abort(404) # Should not happen if DB is consistent
         
    if not current_user.is_admin and visit_record.seller_id != current_user.id:
        return abort(403)
        
    upload_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "visits")
    return send_from_directory(upload_folder, filename)

# Add routes for editing/deleting visits later if needed

