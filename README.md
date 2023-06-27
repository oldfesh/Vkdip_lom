
<div><p>Все слышали про известное приложение для знакомств - Tinder. Приложение предоставляет простой интерфейс для выбора понравившегося человека. Сейчас в Google Play более 100 миллионов установок.</p>
<p>Используя данные из VK, нужно сделать сервис намного лучше, чем Tinder, а именно: чат-бота “VKinder”. Бот должен искать людей, подходящих под условия, на основании информации о пользователе из VK:</p>
<ul>
<li>Возраст,</li>
<li>пол,</li>
<li>город,</li>
<li>семейное положение.</li>
</ul>
<p>У тех людей, которые подошли по требованиям пользователю, получать топ-3 популярных фотографии профиля и отправлять их пользователю в чат вместе со ссылкой на найденного человека.<br>
Популярность определяется по количеству лайков и комментариев.</p>
<p><strong>Входные данные</strong></p>
<ul>
<li>Имя пользователя или его id в ВК, для которого мы ищем пару.</li>
</ul>
<p>если информации недостаточно нужно дополнительно спросить её у пользователя.</p>
<p><strong>Требования к сервису:</strong></p>
<ol>
<li>Код программы удовлетворяет <code>PEP8</code>.</li>
<li>Получать токен от пользователя с нужными правами.</li>
<li>Программа декомпозирована на функции/классы/модули/пакеты.</li>
<li>Результат программы записывать в БД.</li>
<li>Люди не должны повторяться при повторном поиске.</li>
<li>Не запрещается использовать внешние библиотеки для vk.</li>
</ol>
<p><strong>Дополнительные требования (не обязательны для получения диплома):</strong></p>
<ol>
<li>В vk максимальная выдача при поиске 1000 человек. Подумать как это ограничение можно обойти.</li>
<li>Добавить возможность ставить/убирать лайк, выбранной фотографии.</li>
<li>Можно усложнить поиск добавив поиск по интересам. Разбор похожих интересов(группы, книги, музыка, интересы) нужно будет провести с помощью анализа текста.</li>
<li>У каждого критерия поиска должны быть свои веса. То есть совпадение по возрасту должны быть важнее общих групп. Интересы по музыке важнее книг. Наличие общих друзей важнее возраста. И так далее.</li>
<li>Добавлять человека в избранный список, используя БД.</li>
<li>Добавлять человека в черный список чтобы он больше не попадался при поиске, используя БД.</li>
<li>К списку фотографий из аватарок добавлять список фотографий, где отмечен пользователь.</li>
</ol>
</div>
