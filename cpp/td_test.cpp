//
// Copyright Aliaksei Levin (levlam@telegram.org), Arseny Smirnov (arseny30@gmail.com) 2014-2018
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
#include <td/telegram/Client.h>
#include <td/telegram/Log.h>
#include <td/telegram/td_api.h>
#include <td/telegram/td_api.hpp>

#include <cstdint>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <sstream>
#include <string>
#include <vector>

// Simple single-threaded example of TDLib usage.
// Real world programs should use separate thread for the user input.
// Example includes user authentication, receiving updates, getting chat list and sending text messages.

// overloaded

namespace td_api = td::td_api;

using Object = td_api::object_ptr<td_api::Object>;
std::unique_ptr<td::Client> client_;

td_api::object_ptr<td_api::AuthorizationState> authorization_state_;
bool are_authorized_{false};
std::uint64_t current_query_id_{0};
std::uint64_t authentication_query_id_{0};

std::map<std::int32_t, td_api::object_ptr<td_api::user>> users_;

std::map<std::int64_t, std::string> chat_title_;

void restart() {
    client_.reset();
}

std::uint64_t next_query_id() {
    return ++current_query_id_;
}

void send_query(td_api::object_ptr<td_api::Function> f) {
    auto query_id = next_query_id();
    client_->send({query_id, std::move(f)});
}

void on_authorization_state_update();

void process_update(td_api::object_ptr<td_api::Object> update) {
    switch (update->get_id()) {
    case td_api::updateAuthorizationState::ID:
        authorization_state_ =
            std::move(
                static_cast<td_api::updateAuthorizationState &>(*update).authorization_state_
            );
        on_authorization_state_update();
        break;
    default:
        break;
    }
}

void check_authentication_error(Object object) {
    if (object->get_id() == td_api::error::ID) {
        auto error = td::move_tl_object_as<td_api::error>(object);
        std::cerr << "Error: " << to_string(error);
        on_authorization_state_update();
    }
}

void process_response(td::Client::Response response) {
    if (!response.object) {
        return;
    }
    //std::cerr << response.id << " " << to_string(response.object) << std::endl;
    if (response.id == 0) {
        return process_update(std::move(response.object));
    }

    if (response.id == authentication_query_id_) {
        check_authentication_error(std::move(response.object));
    }
}

std::string get_user_name(std::int32_t user_id) {
    auto it = users_.find(user_id);
    if (it == users_.end()) {
        return "unknown user";
    }
    return it->second->first_name_ + " " + it->second->last_name_;
}

void on_authorization_state_update() {
    authentication_query_id_++;
    switch(authorization_state_->get_id()) {
    case td_api::authorizationStateReady::ID:
        are_authorized_ = true;
        std::cerr << "Got authorization" << std::endl;
        break;
    case td_api::authorizationStateClosing::ID:
        std::cerr << "Closing" << std::endl;
        are_authorized_ = false;
        std::cerr << "Terminated" << std::endl;
        break;
    case td_api::authorizationStateWaitCode::ID:
    {
        auto wait_code = std::move(static_cast<td_api::authorizationStateWaitCode &>(*authorization_state_));
        std::string first_name;
        std::string last_name;
        if (!wait_code.is_registered_) {
            std::cerr << "Enter your first name: ";
            std::cin >> first_name;
            std::cerr << "Enter your last name: ";
            std::cin >> last_name;
        }
        std::cerr << "Enter authentication code: ";
        std::string code;
        std::cin >> code;
        send_query(td_api::make_object<td_api::checkAuthenticationCode>(code, first_name, last_name));
    }
    break;
    case td_api::authorizationStateWaitPassword::ID:
    {
        std::cerr << "Enter authentication password: ";
        std::string password;
        std::cin >> password;
        send_query(td_api::make_object<td_api::checkAuthenticationPassword>(password));
    }
    break;
    case td_api::authorizationStateWaitPhoneNumber::ID:
    {
        std::cerr << "Enter phone number: ";
        std::string phone_number;
        std::cin >> phone_number;
        send_query(td_api::make_object<td_api::setAuthenticationPhoneNumber>(
                       phone_number, false /*allow_flash_calls*/, false /*is_current_phone_number*/)
        );
    }
    break;
    case td_api::authorizationStateWaitEncryptionKey::ID:
        send_query(td_api::make_object<td_api::checkDatabaseEncryptionKey>(""));
        break;
    case td_api::authorizationStateWaitTdlibParameters::ID:
    {
        td_api::tdlibParameters parameters;
        parameters.database_directory_ = "tdlib";
        parameters.use_message_database_ = true;
        parameters.use_secret_chats_ = true;
        parameters.api_id_ = 260555;
        parameters.api_hash_ = "9ed45def5d08193d0783b0205f54e299";
        parameters.system_language_code_ = "en";
        parameters.device_model_ = "Desktop";
        parameters.system_version_ = "Unknown";
        parameters.application_version_ = "1.0";
        parameters.enable_storage_optimizer_ = true;
        td_api::setTdlibParameters setParameters(parameters))
        send_query(parameters);
    }
    break;
    default:
        break;
    }
}

int main() {
    td::Log::set_verbosity_level(1);
    bool are_authorized_ = false;
    std::unique_ptr<td::Client> client_ = std::make_unique<td::Client>();

    while (!are_authorized_) {
        process_response(client_->receive(10));
    }

    std::cerr << "Shutting down" << std::endl;
}
