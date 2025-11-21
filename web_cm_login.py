#!/usr/bin/env python3
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from connect import get_connection
import oracledb

cm_bp = Blueprint('cm', __name__, template_folder='templates')


@cm_bp.route('/', methods=['GET'])
def index():
    return render_template('cm_login.html')


@cm_bp.route('/login', methods=['POST'])
def login():
    empid = request.form.get('empid', '').strip()
    password = request.form.get('password', '').strip()

    if not (empid and password):
        flash('All fields are required.', 'error')
        return redirect(url_for('.index'))

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT PASSWORD FROM CONTENT_MANAGER WHERE EMPLOYEE_ID = :e", {"e": empid})
        row = cur.fetchone()

        if row is None:
            flash(f"Employee ID '{empid}' does not exist.", 'warning')
            return redirect(url_for('.index'))

        stored_password = row[0]
        if stored_password != password:
            flash('Incorrect password.', 'warning')
            return redirect(url_for('.index'))

        return render_template('login_result.html', employee_id=empid, success=True)

    except oracledb.Error as e:
        flash(f"Database error: {e}", 'error')
        return redirect(url_for('.index'))

    finally:
        if cur is not None:
            try:
                cur.close()
            except:
                pass
        if conn is not None:
            try:
                conn.close()
            except:
                pass


@cm_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    empid = (data.get('employee_id') or data.get('empid') or '').strip()
    password = (data.get('password') or '').strip()

    if not (empid and password):
        return jsonify({'code': None, 'error': 'All fields required'}), 400

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT PASSWORD FROM CONTENT_MANAGER WHERE EMPLOYEE_ID = :e", {"e": empid})
        row = cur.fetchone()
        if row is None:
            return jsonify({'code': 0, 'employee_id': None}), 404

        stored_password = row[0]
        if stored_password != password:
            return jsonify({'code': None, 'error': 'Incorrect password'}), 401

        return jsonify({'code': 2, 'employee_id': empid})

    except oracledb.Error as e:
        return jsonify({'code': None, 'error': str(e)}), 500

    finally:
        if cur is not None:
            try:
                cur.close()
            except:
                pass
        if conn is not None:
            try:
                conn.close()
            except:
                pass
