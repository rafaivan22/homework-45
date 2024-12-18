import openpyxl
from datetime import datetime

class Test1Results:
    # Класс атрибут для дедлайна
    deadline = "2024-10-28 23:59:59"

    def __init__(self, student_id, file_path="test_1.xlsx"):
        """
        Инициализация с файлом Excel и ID студента (ИСУ).

        :param file_path: путь к .xlsx файлу
        :param student_id: ID студента (номер ИСУ)
        """
        self.file_path = file_path
        self.student_id = student_id
        self.data = self._load_data()

        # Поиск данных для конкретного студента и извлечение нужной информации
        self.grade = None
        self.timestamp = None

        for entry in self.data:
            if entry["ИСУ"] == student_id:
                self.grade = entry["grade"]
                self.timestamp = entry["timestamp"]
                break

        if self.grade is None or self.timestamp is None:
            raise ValueError(f"Student with ISU {student_id} not found in the file.")

    def _load_data(self):
        """
        Загрузка данных из Excel файла с использованием openpyxl.
        """
        data = []
        workbook = openpyxl.load_workbook(self.file_path)
        sheet = workbook.active

        # Предположим, что первая строка - заголовки
        headers = {column.value: column.column for column in sheet[1]}

        # Проверка наличия необходимых заголовков
        required_headers = {"ФИО", "ИСУ", "timestamp", "grade"}
        if not required_headers.issubset(headers.keys()):
            raise ValueError("Некоторые заголовки отсутствуют в файле Excel.")

        for row in sheet.iter_rows(min_row=2, values_only=True):
            entry = {
                "ФИО": row[headers["ФИО"] - 1],
                "ИСУ": row[headers["ИСУ"] - 1],
                "timestamp": self.str_to_timestamp(row[headers["timestamp"] - 1]),
                "grade": row[headers["grade"] - 1]
            }
            data.append(entry)

        return data

    @staticmethod
    def str_to_timestamp(str_):
        return datetime.strptime(str_, "%Y-%m-%d %H:%M:%S")

    def is_late(self):
        """
        Проверяет, была ли отправка студента позднее дедлайна.

        :return: True если self.timestamp позже, чем Test1Results.deadline, иначе False
        """
        deadline_datetime = self.str_to_timestamp(Test1Results.deadline)
        submission_datetime = self.timestamp
        return submission_datetime > deadline_datetime

# Пример использования
if __name__ == "__main__":
    # Убедитесь, что у вас есть правильный номер ИСУ, который существует в таблице
    student_id = 123456  # замените на существующий номер ИСУ

    try:
        test_results = Test1Results(student_id, "test_1.xlsx")

        print(f"Grade for student {test_results.student_id}: {test_results.grade}")

        is_late = test_results.is_late()
        print(f"Was the submission late? {'Yes' if is_late else 'No'}")
    except ValueError as e:
        print(e)