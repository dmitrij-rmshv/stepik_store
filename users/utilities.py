def fb_topics():
    """
    Предлагаемые темы обратной связи пользователей.
    Для использования в users/models/Feedback users/forms/UserFeedbackForm.
    """
    OTHER = 0
    COMPLAINT = 1
    OFFER = 2
    WISH = 3
    QUESTION = 4
    DELETING = 5
    TOPICS = (
        (OTHER, 'обращение вне тем'),
        (COMPLAINT, 'жалоба'),
        (OFFER, 'предложение'),
        (WISH, 'пожелание'),
        (QUESTION, 'вопрос'),
        (DELETING, 'заявка на удаление аккаунта'),
    )
    return TOPICS


def fb_statuses():
    """
    Предлагаемые статусы обработки обратной связи пользователей.
    Для использования в users/models/Feedback users/views/FeedbackDetailView.
    """
    UNWATCHED = 0
    VIEWED = 1
    REJECTED = 2
    ON_THE_GO = 3
    DONE = 4
    STATUSES = (
        (UNWATCHED, 'не просмотрено'),
        (VIEWED, 'просмотрено'),
        (REJECTED, 'отклонено'),
        (ON_THE_GO, 'в работе'),
        (DONE, 'отработано'),
    )
    return STATUSES
