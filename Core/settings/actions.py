class ACTIONS_NAMES:
    TURN_ON_PUMP = "TURN_ON_PUMP"
    OPEN_VALVE = "OPEN_VALVE"
    CLOSE_VALVE = "CLOSE_VALVE"
    CLOSE_ALL_VALVES = "CLOSE_ALL_VALVES"

    FULL_OPEN_RRG = "FULL_OPEN_RRG"
    FULL_CLOSE_RRG = "FULL_CLOSE_RRG"
    SET_RRG_VALUE = "SET_RRG_VALUE"
    SET_RRG_VALUE_WITH_PAUSE = "SET_RRG_VALUE_WITH_PAUSE"
    SET_RRG_AND_KEEP_TO_PRESSURE = "SET_RRG_AND_KEEP_TO_PRESSURE"

    PUMP_OUT_CAMERA = "PUMP_OUT_CAMERA"
    VENTILATE_CAMERA = "VENTILATE_CAMERA"
    SMALL_PUMP_OUT_CAMERA = "SMALL_PUMP_OUT_CAMERA"

    TURN_ON_ALL_TERMODATS = "TURN_ON_ALL_TERMODATS"
    TURN_OFF_ALL_TERMODATS = "TURN_OFF_ALL_TERMODATS"
    SET_T_V_ALL_TERMODATS = "SET_T_V_ALL_TERMODATS"
    WAIT_TARGET_TEMPERATURE = "WAIT_TARGET_TEMPERATURE"

    SET_TEMPERATURE = "SET_TEMPERATURE"
    SET_TEMPERATURE_IN_TIME = "SET_TEMPERATURE_IN_TIME"
    SET_TEMPERATURE_FOR_TERMODAT_DEVICE = "SET_TEMPERATURE_FOR_TERMODAT_DEVICE"
    SET_SPEED_FOR_TERMODAT_DEVICE = "SET_SPEED_FOR_TERMODAT_DEVICE"

    PAUSE = "PAUSE"
    QUICK_SHUTDOWN_DEVICE = "QUICK_SHUTDOWN_DEVICE"

    FULL_OPEN_PUMP = "FULL_OPEN_PUMP"
    FULL_CLOSE_PUMP = "FULL_CLOSE_PUMP"
    STABILIZE_PRESSURE = "STABILIZE_PRESSURE"


class TABLE_ACTIONS_NAMES:
    TURN_ON_PUMP = "Включить насос"

    OPEN_VALVE = "Открыть клапан" + " [клапан]"
    CLOSE_VALVE = "Закрыть клапан" + " [клапан]"
    CLOSE_ALL_VALVES = "Закрыть все клапаны"

    FULL_OPEN_RRG = "Полностью открыть РРГ" + " [газ]"
    FULL_CLOSE_RRG = "Полностью закрыть РРГ" + " [газ]"
    SET_RRG_VALUE = "Значение на РРГ" + " [газ, sccm]"
    SET_RRG_VALUE_WITH_PAUSE = "Значение на РРГ с паузой" + " [газ, sccm, мммм:сс]"
    SET_RRG_AND_KEEP_TO_PRESSURE = "Повысить давление газа на определённую величину [газ, sccm, давление]"

    PUMP_OUT_CAMERA = "Откачать камеру" + " [давление, лимит времени]"
    VENTILATE_CAMERA = "Провентилировать камеру" + " [x, y, температура]"
    SMALL_PUMP_OUT_CAMERA = "Откачать камеру игольчатым вентилем" + " [давление, лимит времени]"

    TURN_ON_ALL_TERMODATS = "Включить все печки"
    TURN_OFF_ALL_TERMODATS = "Выключить все печки"
    SET_T_V_ALL_TERMODATS = "Установить T и V на печки" + " [температура, скорость]"
    WAIT_TARGET_TEMPERATURE = "Ждать установления температуры [температура, мммм:сс]"

    SET_TEMPERATURE = "Установить температуру"
    SET_TEMPERATURE_IN_TIME = "Установить температуру за время"
    SET_TEMPERATURE_FOR_TERMODAT_DEVICE = "Установить температуру (термодат)"
    SET_SPEED_FOR_TERMODAT_DEVICE = "Установить скорость (термодат)"

    PAUSE = "Пауза" + " [время мммм:сс]"
    QUICK_SHUTDOWN_DEVICE = "Полное выключение установки"

    FULL_OPEN_PUMP = "Открыть клапан насоса"
    FULL_CLOSE_PUMP = "Закрыть клапан насоса"
    STABILIZE_PRESSURE = "Стабилизировать давление"
