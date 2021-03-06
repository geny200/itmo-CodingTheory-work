# Домашние работы

## [**Содержание**](./../README.md)

* **Дз 1. Спасение из пиратского плена**
* Дз 2. Двоичный симметричный канал со стираниями (not implemented)
* [**Дз 3. Систематическое кодирование полярных кодов**](./spe.md)

## Условие

Пираты захватили судно с экипажем из ***n = 2^m − 1*** человека. Отчаявшись получить выкуп, они приняли решение
избавиться от заложников. Главарь пиратов сгенерировал ***n*** независимых двоичных равномерно распределенных случайных
значений ***x_i***. Заложники размещаются в одиночных камерах. Главарь сообщает ***i***-ому заложнику значения ***x_j,
j≠i*** вместе с их номерами ***j*** и предлагает угадать значение ***x_i***. Заложник может дать ответы 0, 1 и "не знаю"
. В том случае, если все заложники дают ответ "не знаю"  или любой из них оглашает неправильное значение ***x_i***, всех
заложников казнят. В противном случае все заложники будут освобождены. После оглашения условий этой игры, но до
распределения заложников по камерам и выдачи значений ***x_j***, заложникам разрешается встретиться и выработать
стратегию действий. Необходимо:

* Предложить стратегию действий заложников, максимизирующую вероятность их спасения.
* Оценить кровожадность пиратов, т.е. вероятность казни заложников при использовании ими предложенной стратегии.

## Решение

Любая стратегия для любого исходного вектора (загаданное число из 0 и 1 пиратами) даёт два исхода – положительный, когда
заложников отпускают, и отрицательный, когда не отпускают; тогда т.к. все вектора являются равновероятными, получить
вероятность положительного исхода для стратегии можно через отношение количества положительных исходов, к общему числу
возможных векторов т.е.: P = X/N (X – позитивные исходы, N – всего исходов N = 2^n)

#### Рассмотрим некую оптимальную стратегию:

Есть (N – X) проигрышей, и X выигрышей; выигрыш происходит только при наличии верных угадываний среди заложников, т.е. у
нас X правильных угадываний, а значит столько же ошибочных. Оптимальная стратегия минимизирует количество правильных
угадываний на векторе, и максимизирует неправильные на одном. Тогда можно получить X позитивных исходов и как минимум
X/n отрицательных (т.к. на одном векторе максимум n ошибочных угадываний). Запишем это в виде неравенства:

* (проигрыши) N – X >= X/n (отрицательные исходы ~ проигрыши), где N = 2^n; перепишем
* X <= (n * 2^n) / (n + 1); X/N <= n/(n+1) т.е. вероятность позитивного исхода ***P <= n/(n + 1)***

#### Предлагаемая стратегия:

Пусть вектор являющийся кодом Хэмминга для текущего n, является отрицательным исходом, а вектор не являющийся –
положительным исходом (очевидно, что положительных больше чем отрицательных, и вероятность положительного исхода
запишется как P = n/(n+1) т.к. на каждый вектор числа хэмминга приходится n соседних векторов отрицательного исхода и
данные множества соседей не пересекаются; то данная стратегия оптимальна по P из предыдущих рассуждений).

**Алгоритм выбора для одного заложника**:

- Если при подстановке цифры 1 или 0 получаем число Хэмминга, то отвечаем обратное для числа.
- Иначе отвечаем “не знаю”

##### Пояснения:

Если пираты загадали вектор число являющееся для текущего n числом Хэмиинга, то мы проиграли (все ответили неверно).
Если загадали не число хэмминга - то какой-то заложник отвечает число, значит для текущего вектора при на расстоянии 1
находится число хэмминга и оно единственное, значит ответит только данный заложник и ответит правильно (остальные
ответят не знаю). Ситуации когда будет не число хэмминга и никто не ответит невозможна (значит все соседние числа не
числа хэмминга, а в оптимальной n=2^m-1 такого нет).

#### Ответ:

* Вероятность выигрыша P =n/(n+1) = ***1 - 1/2^m***
* Тогда кровожадность пиратов (вероятность проигрыша) = 1 - P = ***1/2^m***