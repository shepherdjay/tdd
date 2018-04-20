from django.utils.html import escape
from lists.forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
from lists.models import Item, List

import pytest

pytestmark = pytest.mark.django_db


class TestHomePage:
    def test_home_page_renders_home_template(self, client):
        response = client.get('/')
        pytest.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self, client):
        response = client.get('/')
        assert isinstance(response.context['form'], ItemForm)


class TestListView:

    def post_invalid_input(self, client):
        list_ = List.objects.create()
        return client.post(
            '/lists/{}/'.format(list_.id),
            data={'text': ''}
        )

    def test_uses_list_templates(self, client):
        list_ = List.objects.create()
        response = client.get('/lists/{}/'.format(list_.id))
        pytest.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self, client):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = client.get('/lists/{}/'.format(correct_list.id))

        pytest.assertContains(response, 'itemey 1')
        pytest.assertContains(response, 'itemey 2')
        pytest.assertNotContains(response, 'other list item 1')
        pytest.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = client.get('/lists/{}/'.format(correct_list.id))

        assert correct_list == response.context['list']

    def test_displays_item_form(self, client):
        list_ = List.objects.create()
        response = client.get('/lists/{}/'.format(list_.id))
        assert isinstance(response.context['form'], ExistingListItemForm)
        pytest.assertContains(response, 'name="text"')

    def test_can_save_a_POST_request_to_an_existing_list(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        client.post(
            '/lists/{}/'.format(correct_list.id),
            data={'text': 'A new item for an existing list'}
        )

        assert 1 == Item.objects.count()
        new_item = Item.objects.first()
        assert 'A new item for an existing list' == new_item.text
        assert correct_list == new_item.list

    def test_POST_redirects_to_list_view(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = client.post(
            '/lists/{}/'.format(correct_list.id),
            data={'text': 'A new item for an existing list'}
        )
        pytest.assertRedirects(response, '/lists/{}/'.format(correct_list.id))

    def test_for_invalid_input_nothing_saved_to_db(self, client):
        self.post_invalid_input(client)
        assert 0 == Item.objects.count()

    def test_for_invalid_input_renders_list_template(self, client):
        response = self.post_invalid_input(client)
        assert 200 == response.status_code
        pytest.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self, client):
        response = self.post_invalid_input(client)
        assert isinstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self, client):
        response = self.post_invalid_input(client)
        pytest.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self, client):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = client.post(
            '/lists/%d/' % (list1.id,),
            data={'text': 'textey'}
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        pytest.assertContains(response, expected_error)
        pytest.assertTemplateUsed(response, 'list.html')
        assert 1 == Item.objects.all().count()


class TestNewList:
    def test_saving_a_POST_request(self, client):
        client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )

        assert 1 == Item.objects.count(), 1
        new_item = Item.objects.first()
        assert 'A new list item' == new_item.text

    def test_redirects_after_POST(self, client):
        response = client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )
        new_list = List.objects.first()
        pytest.assertRedirects(response, '/lists/{}/'.format(new_list.id))

    def test_for_invalid_input_renders_home_template(self, client):
        response = client.post('/lists/new', data={'text': ''})
        assert 200 == response.status_code
        pytest.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self, client):
        response = client.post('/lists/new', data={'text': ''})
        pytest.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self, client):
        response = client.post('/lists/new', data={'text': ''})
        assert isinstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self, client):
        client.post('/lists/new', data={'text': ''})
        assert 0 == List.objects.count()
        assert 0 == Item.objects.count()
