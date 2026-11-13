"""Testes da interface simulada pelo Streamlit. Sem conta ou chamada externa."""
import os
from pathlib import Path
import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import land_core as land

APP = str(Path(__file__).with_name('app.py'))


class AppTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {'OPENAI_API_KEY':'', 'OPENAI_MODEL':''})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.app = AppTest.from_file(APP, default_timeout=15).run()
        self.assertEqual(len(self.app.exception), 0)

    def test_offline_run_edit_and_reset(self):
        app = self.app
        with patch('land_core.call_model') as model:
            app.button('run').click().run()
            model.assert_not_called()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.dataframe[0].value), 3)
        app.text_area('excerpt_0').set_value('Recorte alterado pelo aluno.').run()
        self.assertEqual(len(app.dataframe), 0)
        self.assertTrue(any('alterou' in item.value for item in app.info))
        app.button('run').click().run()
        self.assertEqual(app.dataframe[0].value.iloc[0]['Evidência literal'], 'Recorte alterado pelo aluno.')
        app.button('reset').click().run()
        self.assertEqual(len(app.dataframe), 0)
        self.assertTrue(app.text_area('excerpt_0').value.startswith('Caixa de entrada'))

    def test_source_add_remove_and_invalid_input(self):
        app = self.app
        app.button('add').click().run()
        self.assertEqual(app.session_state['source_count'], 4)
        self.assertTrue(app.button('run').disabled)
        app.button('remove').click().run()
        self.assertFalse(app.button('run').disabled)
        app.text_area('question').set_value('').run()
        self.assertTrue(app.button('run').disabled)
        self.assertGreater(len(app.warning), 0)

    def test_model_requires_explicit_click_and_handles_failure(self):
        app = self.app
        with patch('land_core.call_model') as model:
            app.radio('mode').set_value('Com IA').run()
            self.assertTrue(app.button('run').disabled)
            app.text_input('model').set_value('modelo-de-teste').run()
            app.text_input('api_key').set_value('credencial-ficticia').run()
            self.assertTrue(app.button('run').disabled)
            app.checkbox('consent').check().run()
            model.assert_not_called()
            self.assertFalse(app.button('run').disabled)
            model.side_effect = lambda q,c,m,k: (land.organize_offline(q,c), {'total_tokens':600})
            app.button('run').click().run()
            model.assert_called_once()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(len(app.dataframe), 1)
            model.side_effect = land.LandError('Falha simulada de conexão.')
            app.button('run').click().run()
            self.assertEqual(len(app.dataframe), 0)
            self.assertIn('simulada', app.error[0].value)
            self.assertEqual(len(app.exception), 0)

    def test_mode_change_clears_previous_result(self):
        self.app.button('run').click().run()
        self.app.radio('mode').set_value('Com IA').run()
        self.assertEqual(len(self.app.dataframe), 0)
        self.assertTrue(self.app.button('run').disabled)


if __name__ == '__main__':
    unittest.main()
