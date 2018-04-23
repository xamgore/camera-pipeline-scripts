#!/bin/bash
# Default acpi script that takes an entry for all actions

SEND_MESSAGE=/home/xi/au-camera-scripts/power_status/send_message.py

case "$1" in
    ac_adapter)
        case "$2" in
            AC*|ACAD|ADP0)
                case "$4" in
                    00000000)
                        logger 'AC unpluged'
                        python "$SEND_MESSAGE" ':electric_plug: AC unpluged'
                        ;;
                    00000001)
                        logger 'AC pluged'
                        python "$SEND_MESSAGE" ':electric_plug: AC pluged'
                        ;;
                esac
                ;;
            *)
                logger "ACPI action undefined: $2"
                ;;
        esac
        ;;
    button/lid)
        case "$3" in
            close)
                logger 'LID closed'
                python "$SEND_MESSAGE" ':computer: LID closed'
                ;;
            open)
                logger 'LID opened'
                python "$SEND_MESSAGE" ':computer: LID opened'
                ;;
            *)
                logger "ACPI action undefined: $3"
                ;;
    esac
    ;;
    *)
        logger "ACPI group/action undefined: $1 / $2"
        ;;
esac

# vim:set ts=4 sw=4 ft=sh et:
