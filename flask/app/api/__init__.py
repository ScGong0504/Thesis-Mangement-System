from .account import get_auth_token_user, set_auth_pwd_admin, account_register, name_not_in_db, \
    get_auth_token_admin, get_verify_code
from .authentication import verify_password_admin, unauthorized, verify_password_user
from .user_manage import get_user_list, remove_user, batchremove_user, set_user_permit
from .paper_manage import query_papers, query_lot_paper_by_titles
from .comment import get_comment_list, add_comment, add_reply, delete_comment, delete_reply
from .note import get_note_list, add_note, can_i_add_note, delete_note
from .domain_manage import get_domain_list, add_domain_list, delete_domain, update_domain
from .paper_view import paper_details, get_mypaper_list, post_paper, update_paper, delete_paper
from .data_graph import domain_pic
