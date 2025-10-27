import csv
from django.core.management.base import BaseCommand, CommandError
from quiz.models import Question
import os

class Command(BaseCommand):
    help = '指定されたCSVファイルからTOEIC問題を一括インポートします。'

    def add_arguments(self, parser):
        # コマンドがCSVファイルのパスを引数として受け取れるようにする
        parser.add_argument('csv_file_path', type=str, help='インポートするCSVファイルのパス')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']

        # ファイルの存在チェック
        if not os.path.exists(csv_file_path):
            raise CommandError(f"ファイルが見つかりません: {csv_file_path}")

        # CSVファイルを開く (UTF-8 BOM付きにも対応)
        try:
            with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                
                # CSVのヘッダー（列名）がモデルと一致しているか簡易チェック
                expected_headers = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'explanation', 'part', 'difficulty_level']
                if not all(header in reader.fieldnames for header in expected_headers):
                    self.stdout.write(self.style.ERROR('CSVのヘッダーが正しくありません。'))
                    self.stdout.write(self.style.WARNING(f"必須ヘッダー: {expected_headers}"))
                    self.stdout.write(self.style.WARNING(f"検出されたヘッダー: {reader.fieldnames}"))
                    return

                count_created = 0
                count_updated = 0

                for row in reader:
                    # 難易度を整数に変換（空の場合はデフォルト値が使われるようにNone）
                    try:
                        difficulty = int(row.get('difficulty_level', 600))
                    except (ValueError, TypeError):
                        difficulty = 600 # 変換失敗時はデフォルト600

                    # 解説が空の場合（None）に対応
                    explanation_text = row.get('explanation')
                    if not explanation_text:
                        explanation_text = "" # DBの制約に合わせて空文字に

                    # update_or_create でデータの登録・更新を安全に行う
                    # question_text が一致するものが既にあれば更新、なければ新規作成
                    question, created = Question.objects.update_or_create(
                        question_text=row['question_text'], # 問題文をキーにして重複チェック
                        defaults={
                            'option_a': row['option_a'],
                            'option_b': row['option_b'],
                            'option_c': row['option_c'],
                            'option_d': row['option_d'],
                            'correct_answer': row['correct_answer'],
                            'explanation': explanation_text,
                            'part': row.get('part', 'PART5'), # CSVになければPART5
                            'difficulty_level': difficulty,
                        }
                    )

                    if created:
                        count_created += 1
                    else:
                        count_updated += 1

            self.stdout.write(self.style.SUCCESS(f'インポートが完了しました。'))
            self.stdout.write(self.style.SUCCESS(f'新規作成: {count_created} 件'))
            self.stdout.write(self.style.SUCCESS(f'更新: {count_updated} 件'))

        except FileNotFoundError:
            raise CommandError(f"ファイルが見つかりません: {csv_file_path}")
        except Exception as e:
            raise CommandError(f"インポート中にエラーが発生しました: {e}")