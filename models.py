from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<UploadedFile {self.id}>'
