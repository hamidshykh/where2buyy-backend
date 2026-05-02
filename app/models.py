from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    BigInteger,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.database import Base


# ------------------------------
# STORE MODEL
# ------------------------------
class StoreName(Base):
    __tablename__ = "store_name"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    store_name = Column(String(128), nullable=False)
    store_description = Column(String(1024))

    # Relationship with products
    product = relationship("Product", back_populates="store")


# ------------------------------
# BRAND MODEL
# ------------------------------
class BrandName(Base):
    __tablename__ = "brand_name"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    brand_name = Column(String(128), nullable=False)
    brand_description = Column(String(1024))

    # Relationship with products
    product = relationship("Product", back_populates="brand")


# ------------------------------
# CATEGORY MODEL
# ------------------------------
class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(128), nullable=False)
    category_description = Column(String(512))

    # Relationship with products
    product = relationship("Product", back_populates="category_rel")




class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    url = Column(String(1024))
    category = Column(Integer, ForeignKey("categories.id"))
    image = Column(String(1024))
    price = Column(Float)
    brand_name = Column(Integer, ForeignKey("brand_name.id"))   # ✅ FIXED
    store_name = Column(Integer, ForeignKey("store_name.id"))   # ✅ FIXED
    product_attribute = Column(String(128))
    product_description = Column(Text)
    product_specification = Column(Text)
    submitted_by = Column(String(256))
    vote_count = Column(Integer)
    comment_count = Column(Integer)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    status = Column(Boolean)
    product_slugs = Column(Text)
    expiry_date = Column(DateTime)

    # Relationships
    brand = relationship("BrandName", back_populates="product")
    store = relationship("StoreName", back_populates="product")
    category_rel = relationship("Categories", back_populates="product")
    votes = relationship("ProductVotes", back_populates="product")
    comments = relationship("ProductComments", back_populates="product")


# ------------------------------
# PRODUCT VOTES MODEL
# ------------------------------
class ProductVotes(Base):
    __tablename__ = "product_votes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("product.id"))  # ✅ lowercase
    user_id = Column(Integer, ForeignKey("auth_user.id"))   # ✅ lowercase
    vote = Column(Integer, nullable=False)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)

    product = relationship("Product", back_populates="votes")
    user = relationship("AuthUser", back_populates="votes")

# ------------------------------
# PRODUCT COMMENTS MODEL
# ------------------------------
class ProductComments(Base):
    __tablename__ = "product_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("product.id"))  # ✅ lowercase
    user_id = Column(Integer, ForeignKey("auth_user.id"))   # ✅ lowercase
    comments = Column(Text)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)

    product = relationship("Product", back_populates="comments")
    user = relationship("AuthUser", back_populates="comments")


# ------------------------------
# AUTH USER MODEL
# ------------------------------
class AuthUser(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime)
    is_superuser = Column(Boolean, nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime, nullable=False)
    contact_number = Column(String(11))

    # Relationships
    votes = relationship("ProductVotes", back_populates="user")
    comments = relationship("ProductComments", back_populates="user")
