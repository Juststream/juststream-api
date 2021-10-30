from fastapi import APIRouter

from services.dynamodb_clients.blogs_table import BlogsTable

router = APIRouter(
    prefix='/blogs'
)

blogs_table = BlogsTable()


@router.get('/')
def get_blogs():
    return list(blogs_table.get_all_items())


@router.get('/{blog_id}')
def get_blog(blog_id: str):
    return blogs_table.get_item(blog_id)
