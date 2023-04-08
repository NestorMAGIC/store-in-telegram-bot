-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Апр 08 2023 г., 10:24
-- Версия сервера: 10.4.27-MariaDB
-- Версия PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `shop`
--

-- --------------------------------------------------------

--
-- Структура таблицы `cat`
--

CREATE TABLE `cat` (
  `id` int(11) NOT NULL,
  `cat` varchar(50) NOT NULL,
  `description` varchar(355) NOT NULL,
  `price` int(11) DEFAULT 99,
  `img` varchar(50) NOT NULL DEFAULT 'neuro4.png'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `cat`
--

INSERT INTO `cat` (`id`, `cat`, `description`, `price`, `img`) VALUES
(1, 'Default', '<b>Minecraft</b> лицензия <b>без</b> доступа к почте. После оплаты вам предоставляется логин и пароль от <b>Mojang</b> аккаунта. Магазин <b>несет</b> ответственность, в случае кражи аккаунта мы предоставим вам другой аккаунт из этой категории', 149, 'default.jpg'),
(2, 'Premium', '<b>Minecraft</b> лицензия с доступом к почте. После оплаты вам предоставляется логин, пароль, и доступ к электронной почте от <b>Mojang</b> аккаунта. Магазин <b>несет</b> ответственность, в случае кражи аккаунта мы предоставим вам другой аккаунт из этой категории ', 249, 'premium.png');

-- --------------------------------------------------------

--
-- Структура таблицы `codes`
--

CREATE TABLE `codes` (
  `id` int(11) NOT NULL,
  `code` varchar(50) NOT NULL,
  `discount` int(255) NOT NULL,
  `money` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `codes`
--

INSERT INTO `codes` (`id`, `code`, `discount`, `money`) VALUES
(1, 'MAGIC', 25, 434);

-- --------------------------------------------------------

--
-- Структура таблицы `items`
--

CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `cat` varchar(50) NOT NULL DEFAULT 'Default',
  `email` varchar(50) DEFAULT NULL,
  `email_password` varchar(50) DEFAULT NULL,
  `login` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'in stock'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `items`
--

INSERT INTO `items` (`id`, `cat`, `email`, `email_password`, `login`, `password`, `status`) VALUES
(2, 'Premium', 'example@test.com', '1234554321', 'nestorMAGIC', 'Leopold2008_', 'completed'),
(3, 'Default', NULL, NULL, 'Nestor2008', 'leopold29052008', 'in proccess'),
(4, 'Premium', 'nestor-davydkin@mail.ru', 'jkfjdlsLKDSJF;sdfjewdf.dsf', 'Herobrine', 'nestor2008', 'in stock');

-- --------------------------------------------------------

--
-- Структура таблицы `orders`
--

CREATE TABLE `orders` (
  `id` int(50) NOT NULL,
  `order_id` int(50) NOT NULL,
  `user_id` int(50) NOT NULL,
  `item_id` int(50) NOT NULL,
  `price` int(50) NOT NULL,
  `oldprice` int(50) DEFAULT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'in proccess',
  `item_cat` varchar(50) NOT NULL,
  `lifetime` bigint(255) NOT NULL DEFAULT 15
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `orders`
--

INSERT INTO `orders` (`id`, `order_id`, `user_id`, `item_id`, `price`, `oldprice`, `status`, `item_cat`, `lifetime`) VALUES
(124, 811830319, 811801332, 3, 112, 149, 'in proccess', 'Default', 1680439327),
(125, 811843677, 811801332, 2, 187, 249, 'completed', 'Premium', 1680445846);

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `code` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `user_id`, `code`) VALUES
(5, 811801332, 'MAGIC');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `cat`
--
ALTER TABLE `cat`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `codes`
--
ALTER TABLE `codes`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `cat`
--
ALTER TABLE `cat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `codes`
--
ALTER TABLE `codes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `items`
--
ALTER TABLE `items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=126;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
